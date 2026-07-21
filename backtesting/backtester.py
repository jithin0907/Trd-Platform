from providers.data_provider import DataProvider

from backtesting.trade_simulator import TradeSimulator
from backtesting.statistics import Statistics

from engine.strategy_manager import StrategyManager
from datetime import datetime

import MetaTrader5 as mt5
from datetime import datetime


class Backtester:

    def __init__(
        self,
        strategy_name,
        symbol,
        timeframe,
        bars=1000,
        warmup=100
    ):

        self.strategy_name = strategy_name
        self.symbol = symbol
        self.timeframe = timeframe
        self.bars = bars
        self.warmup = warmup

        self.provider = DataProvider()

    def run(self):

        print("\n==========================================")
        print("STARTING BACKTEST")
        print("==========================================")

        if not self.provider.connect():
            return

        # ==========================================
        # LIVE TIME CHECK
        # ==========================================

        print("\n========== LIVE TIME CHECK ==========")

        # PC Local Time
        print("PC Local Time   :", datetime.now())

        # MT5 Server Time
        tick = mt5.symbol_info_tick(self.symbol)
        print("MT5 Server Time :", datetime.fromtimestamp(tick.time))

        # Latest Closed M5 Candle
        latest = self.provider.get_market_data(
            symbol=self.symbol,
            timeframe="M5",
            bars=1
        )
        print(latest)

        print("Latest M5 Candle:", latest.iloc[-1]["time"])
        print("====================================")

        # ==========================================

        df = self.provider.get_market_data(
            symbol=self.symbol,
            timeframe=self.timeframe,
            bars=self.bars
        )

        print("\nBacktest Period")
        print("------------------------------------------")
        print("Symbol      :", self.symbol)
        print("Timeframe   :", self.timeframe)
        print("Bars        :", len(df))
        print("Start Date  :", df.iloc[0]["time"])
        print("End Date    :", df.iloc[-1]["time"])

        strategy = StrategyManager.load(
            self.strategy_name
        )

        signals = 0
        trade_history = []

        # ------------------------------------------
        # Download HTF history once (CRT only)
        # ------------------------------------------

        htf_df = None

        if self.strategy_name == "crt":

            htf_df = self.provider.get_market_data(
                symbol=self.symbol,
                timeframe="H4",
                bars=max(200, self.bars // 48 + 20)
            )

        index = self.warmup

        while index < len(df):

            market = df.iloc[:index + 1].copy()

            # ---------------------------------------
            # Prepare strategy-specific data
            # ---------------------------------------

            if self.strategy_name == "crt":

                current_time = market.iloc[-1]["time"]

                htf_history = htf_df[
                    htf_df["time"] <= current_time
                ].copy()

                if len(htf_history) == 0:
                    index += 1
                    continue

                data = {
                    "htf": htf_history,
                    "entry": market
                }

                print("=" * 80)
                print("BACKTEST")
                print("ENTRY LAST TIME :", data["entry"].iloc[-1]["time"])
                print("ENTRY LAST CLOSE:", data["entry"].iloc[-1]["close"])

                print("HTF LAST TIME   :", data["htf"].iloc[-1]["time"])
                print("HTF LAST CLOSE  :", data["htf"].iloc[-1]["close"])

                print("ENTRY BARS :", len(data["entry"]))
                print("HTF BARS   :", len(data["htf"]))
                print("=" * 80)


                signal = strategy.analyze(
                    self.symbol,
                    self.timeframe,
                    data
                )

            else:

                signal = strategy.analyze(
                    self.symbol,
                    self.timeframe,
                    market
                )

            if signal.signal:

                signals += 1

                result = TradeSimulator.simulate(
                    df,
                    index,
                    signal
                )

                trade_history.append(result)

                print("\n------------------------------------------")
                print("Entry Time :", result["entry_time"])
                print("Exit Time  :", result["exit_time"])
                print("Direction  :", signal.direction)
                print("Entry      :", result["entry_price"])
                print("Exit       :", result["exit_price"])
                print("SL         :", result["stop_loss"])
                print("TP         :", result["take_profit"])
                print("Profit (Pips) :", round(result["profit_pips"], 2))
                print("RR         :", round(result["rr"], 2))
                print("Duration   :", result["duration"], "candles")
                print("Result     :", result["result"])

                if result["result"] == "OPEN":
                    break

                # Skip all candles while trade was active
                index = result["exit_index"] + 1

            else:

                index += 1

        stats = Statistics.calculate(trade_history)

        print("\n==========================================")
        print("BACKTEST REPORT")
        print("==========================================")

        print(f"Strategy                : {self.strategy_name}")
        print(f"Symbol                  : {self.symbol}")
        print(f"Timeframe               : {self.timeframe}")

        print("------------------------------------------")

        print(f"Signals Generated       : {signals}")
        print(f"Total Trades            : {stats['total_trades']}")
        print(f"Winning Trades          : {stats['wins']}")
        print(f"Losing Trades           : {stats['losses']}")
        print(f"Open Trades             : {stats['open_trades']}")

        print("------------------------------------------")

        print(f"Win Rate                : {stats['win_rate']:.2f}%")
        print(f"Loss Rate               : {stats['loss_rate']:.2f}%")

        print("------------------------------------------")

        print(f"Gross Profit (Pips)     : {stats['gross_profit']}")
        print(f"Gross Loss (Pips)       : {stats['gross_loss']}")
        print(f"Net Profit (Pips)       : {stats['net_profit']}")

        print("------------------------------------------")

        print(f"Profit Factor           : {stats['profit_factor']}")
        print(f"Average Win (Pips)      : {stats['average_win']}")
        print(f"Average Loss (Pips)     : {stats['average_loss']}")
        print(f"Average RR              : {stats['average_rr']}")

        print("------------------------------------------")

        print(f"Longest Win Streak      : {stats['longest_win_streak']}")
        print(f"Longest Loss Streak     : {stats['longest_loss_streak']}")

        print("==========================================")

        self.provider.shutdown()