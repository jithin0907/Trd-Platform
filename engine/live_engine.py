from providers.data_provider import DataProvider
from engine.strategy_manager import StrategyManager
from execution.trade_executor import TradeExecutor

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

        last_bar_time = None

        # ------------------------------------
        # Load H4 Data Once
        # ------------------------------------

        htf_df = self.provider.get_market_data(

            SYMBOL,

            "H4",

            500

        )

        last_htf_bar = htf_df.iloc[-1]["time"]

        while True:

            # -------------------------------
            # Get latest market data
            # -------------------------------

            entry_df = self.provider.get_market_data(
                SYMBOL,
                TIMEFRAME,
                BARS
            )

            

            if entry_df is None or len(entry_df) == 0:
                time.sleep(1)
                continue

            current_bar = entry_df.iloc[-1]["time"]

            # Wait until a new candle closes
            if current_bar == last_bar_time:
                time.sleep(1)
                continue

            last_bar_time = current_bar

            # ------------------------------------
            # Refresh H4 Only If New H4 Candle
            # ------------------------------------

            latest_htf = self.provider.get_market_data(

                SYMBOL,

                "H4",

                500

            )

            current_htf_bar = latest_htf.iloc[-1]["time"]

            if current_htf_bar != last_htf_bar:

                print("New H4 Candle Detected")

                htf_df = latest_htf

                last_htf_bar = current_htf_bar

            print("\n----------------------------------------")
            print("New Candle :", current_bar)
            print("----------------------------------------")

            # -------------------------------
            # Analyze Strategy
            # -------------------------------


            # ------------------------------------
            # Prepare Strategy Data
            # ------------------------------------

            data = {

                "htf": htf_df,

                "entry": entry_df

            }


            print("=" * 80)
            print("LIVE")
            print("ENTRY LAST TIME :", data["entry"].iloc[-1]["time"])
            print("ENTRY LAST CLOSE:", data["entry"].iloc[-1]["close"])

            print("HTF LAST TIME   :", data["htf"].iloc[-1]["time"])
            print("HTF LAST CLOSE  :", data["htf"].iloc[-1]["close"])

            print("ENTRY BARS :", len(data["entry"]))
            print("HTF BARS   :", len(data["htf"]))
            print("=" * 80)

            # ------------------------------------
            # Analyze Strategy
            # ------------------------------------

            signal = strategy.analyze(

                symbol=SYMBOL,

                timeframe=TIMEFRAME,

                data=data

            )

            # -------------------------------
            # Execute Trade
            # -------------------------------

            if signal.signal:

                print()

                print("BUY/SELL SIGNAL FOUND")

                print(signal.direction)

                self.executor.place_trade(signal)

            else:

                print("No Trade")

            time.sleep(1)