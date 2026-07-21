import MetaTrader5 as mt5
import pandas as pd


class MT5Provider:

    def __init__(self):

        self.connected = False

    # -------------------------------------------------
    # Connect
    # -------------------------------------------------

    def connect(self):

        if not mt5.initialize():
            print("Failed to connect to MT5")
            print(mt5.last_error())
            return False

        self.connected = True

        account = mt5.account_info()

        if account:

            print("-----------------------------------")
            print("Connected to MetaTrader 5")
            print("Account :", account.login)
            print("Server  :", account.server)
            print("Balance :", account.balance)
            print("-----------------------------------")

        return True

    # -------------------------------------------------
    # Shutdown
    # -------------------------------------------------

    def shutdown(self):

        mt5.shutdown()

        self.connected = False

    # -------------------------------------------------
    # Account Info
    # -------------------------------------------------

    def get_account_info(self):

        return mt5.account_info()

    # -------------------------------------------------
    # Symbols
    # -------------------------------------------------

    def get_symbols(self):

        symbols = mt5.symbols_get()

        if symbols is None:
            return []

        return [symbol.name for symbol in symbols]

    # -------------------------------------------------
    # Historical Data
    # -------------------------------------------------

    def get_historical_data(
        self,
        symbol,
        timeframe="M15",
        bars=500
    ):

        timeframe_map = {

            "M1": mt5.TIMEFRAME_M1,
            "M5": mt5.TIMEFRAME_M5,
            "M15": mt5.TIMEFRAME_M15,
            "M30": mt5.TIMEFRAME_M30,
            "H1": mt5.TIMEFRAME_H1,
            "H4": mt5.TIMEFRAME_H4,
            "D1": mt5.TIMEFRAME_D1

        }

        tf = timeframe_map.get(timeframe)

        if tf is None:
            raise ValueError("Unsupported timeframe.")

        rates = mt5.copy_rates_from_pos(
            symbol,
            tf,
            1,
            bars
        )

        if rates is None:

            raise Exception(mt5.last_error())

        df = pd.DataFrame(rates)

        df["time"] = pd.to_datetime(
            df["time"],
            unit="s"
        )


        print("\n===== MT5 PROVIDER =====")
        print("First Candle :", df.iloc[0]["time"])
        print("Last Candle  :", df.iloc[-1]["time"])

        tick = mt5.symbol_info_tick(symbol)

        from datetime import datetime

        print("Last Tick    :", datetime.fromtimestamp(tick.time))
        print("========================\n")

        return df