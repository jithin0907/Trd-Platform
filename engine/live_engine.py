from providers.data_provider import DataProvider
from engine.strategy_manager import StrategyManager
from execution.trade_executor import TradeExecutor
import MetaTrader5 as mt5

from config.settings import *

import time


class LiveEngine:

    def __init__(self):

        self.provider = DataProvider()
        self.executor = TradeExecutor()

    def run(self):

        print("=" * 60)
        print("LIVE TRADING STARTED")
        print("=" * 60)

        if not self.provider.connect():
            print("Unable to connect MT5.")
            return

        strategy = StrategyManager.load(STRATEGY)

        # ------------------------------------
        # State for each symbol
        # ------------------------------------

        last_bar_time = {}
        last_htf_bar = {}
        htf_data = {}

        # ------------------------------------
        # Load initial H4 data for each symbol
        # ------------------------------------

        for symbol in SYMBOLS:

            htf_df = self.provider.get_market_data(
                symbol,
                "H4",
                200
            )

            if htf_df is None or len(htf_df) == 0:

                print(f"Unable to load H4 data for {symbol}")
                continue

            htf_data[symbol] = htf_df
            last_htf_bar[symbol] = htf_df.iloc[-1]["time"]
            last_bar_time[symbol] = None

            # Make sure symbol is available in MT5
            mt5.symbol_select(symbol, True)

            print("----------------------------------------")
            print("Symbol Loaded :", symbol)
            print("H4 Last Time  :", last_htf_bar[symbol])
            print("----------------------------------------")

        # ------------------------------------
        # Main Loop
        # ------------------------------------

        while True:

            for symbol in SYMBOLS:

                # ------------------------------------
                # Skip symbol if H4 data unavailable
                # ------------------------------------

                if symbol not in htf_data:
                    continue

                # ------------------------------------
                # Get latest M5 data
                # ------------------------------------

                entry_df = self.provider.get_market_data(
                    symbol,
                    TIMEFRAME,
                    BARS
                )

                if entry_df is None or len(entry_df) == 0:
                    continue

                current_bar = entry_df.iloc[-1]["time"]

                # ------------------------------------
                # Process only when a new M5 candle appears
                # ------------------------------------

                if current_bar == last_bar_time[symbol]:
                    continue

                last_bar_time[symbol] = current_bar

                print("\n" + "=" * 60)
                print(f"NEW CANDLE : {symbol}")
                print(f"Time       : {current_bar}")
                print("=" * 60)

                # ------------------------------------
                # Refresh H4 data
                # ------------------------------------

                latest_htf = self.provider.get_market_data(
                    symbol,
                    "H4",
                    200
                )

                if latest_htf is None or len(latest_htf) == 0:
                    continue

                current_htf_bar = latest_htf.iloc[-1]["time"]

                # ------------------------------------
                # New H4 candle
                # ------------------------------------

                if current_htf_bar != last_htf_bar[symbol]:

                    print("=" * 60)
                    print(f"NEW H4 CANDLE : {symbol}")
                    print("Cancelling Old Pending Orders...")
                    print("=" * 60)

                    self.executor.cancel_pending_orders(symbol)

                    htf_data[symbol] = latest_htf
                    last_htf_bar[symbol] = current_htf_bar

                # ------------------------------------
                # Prepare strategy data
                # ------------------------------------

                data = {

                    "htf": htf_data[symbol],

                    "entry": entry_df

                }

                # ------------------------------------
                # Debug information
                # ------------------------------------

                print("=" * 80)
                print("LIVE")
                print("SYMBOL          :", symbol)
                print("ENTRY LAST TIME :", data["entry"].iloc[-1]["time"])
                print("ENTRY LAST CLOSE:", data["entry"].iloc[-1]["close"])

                print("HTF LAST TIME   :", data["htf"].iloc[-1]["time"])
                print("HTF LAST CLOSE  :", data["htf"].iloc[-1]["close"])

                print("ENTRY BARS      :", len(data["entry"]))
                print("HTF BARS        :", len(data["htf"]))
                print("=" * 80)

                # ------------------------------------
                # Analyze strategy
                # ------------------------------------

                signal = strategy.analyze(

                    symbol=symbol,

                    timeframe=TIMEFRAME,

                    data=data

                )

                # ------------------------------------
                # Execute trade
                # ------------------------------------

                if signal.signal:

                    print()
                    print("=" * 60)
                    print("BUY/SELL SIGNAL FOUND")
                    print("=" * 60)

                    print("Symbol           :", signal.symbol)
                    print("Direction        :", signal.direction)
                    print("Signal Entry     :", signal.entry)
                    print("Signal SL        :", signal.stop_loss)
                    print("Signal TP        :", signal.take_profit)

                    tick = mt5.symbol_info_tick(signal.symbol)

                    if tick:

                        print("Current Bid      :", tick.bid)
                        print("Current Ask      :", tick.ask)

                        print(
                            "Ask Difference   :",
                            f"{abs(tick.ask - signal.entry):.5f}"
                        )

                        print(
                            "Bid Difference   :",
                            f"{abs(tick.bid - signal.entry):.5f}"
                        )

                    print("=" * 60)

                    self.executor.place_trade(signal)

                else:

                    print(f"No Trade : {symbol}")

            # ------------------------------------
            # Small delay before next scan
            # ------------------------------------

            time.sleep(1)