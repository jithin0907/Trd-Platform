from strategies.base_strategy import BaseStrategy

from models.signal import Signal

from strategies.crt.htf_range import HTFRangeDetector
from strategies.crt.sweep_detector import SweepDetector
from strategies.crt.validation import Validation
from strategies.crt.trade_levels import TradeLevels
from engine.market_structure_engine import MarketStructureEngine
from strategies.crt.config import TP_MODE, RISK_REWARD


class CRTStrategy(BaseStrategy):

    def analyze(
        self,
        symbol,
        timeframe,
        data
    ) -> Signal:

        """
        data should contain

        {
            "htf": h4_dataframe,
            "entry": m5_dataframe
        }
        """

        htf_df = data["htf"]
        entry_df = data["entry"]

        # ---------------------------------
        # HTF Range
        # ---------------------------------

        htf_range = HTFRangeDetector.get(htf_df)

        if htf_range is None:

            return Signal(
                strategy="CRT",
                symbol=symbol,
                timeframe=timeframe
            )

        # ---------------------------------
        # Sweep Detection
        # ---------------------------------

        sweep = SweepDetector.detect(
            entry_df,
            htf_range
        )

        if sweep is None:

            return Signal(
                strategy="CRT",
                symbol=symbol,
                timeframe=timeframe
            )

        # ---------------------------------
        # Validation
        # ---------------------------------

        if not Validation.validate(
            sweep,
            htf_range
        ):

            return Signal(
                strategy="CRT",
                symbol=symbol,
                timeframe=timeframe
            )
        
        # ---------------------------------
        # Market Structure
        # ---------------------------------

        structure_engine = MarketStructureEngine()

        structure = structure_engine.detect(entry_df)

        if not structure["bos"]["valid"]:
            return Signal(
                strategy="CRT",
                symbol=symbol,
                timeframe=timeframe
            )

        if not structure["choch"]["valid"]:
            return Signal(
               strategy="CRT",
               symbol=symbol,
              timeframe=timeframe
         )

      # if not structure["mss"]["valid"]:
       #   return Signal(
        #     strategy="CRT",
         #   symbol=symbol,
          #  timeframe=timeframe
       #)        

        # ---------------------------------
        # Trade Levels
        # ---------------------------------

        levels = TradeLevels.calculate(
        symbol,
         sweep,
         htf_range
        )

        print("\n================ TRADE LEVELS ================")
        print(f"Time          : {entry_df.iloc[-1]['time']}")
        print(f"TP Mode       : {TP_MODE}")
        print(f"RR Config     : {RISK_REWARD}")

        if levels is not None:
            print(f"Entry         : {levels['entry']}")
            print(f"Stop Loss     : {levels['stop_loss']}")
            print(f"Take Profit   : {levels['take_profit']}")
            print(f"Risk Reward   : {levels['risk_reward']}")
        else:
            print("Levels        : None")

        print("=============================================\n")

        # ---------------------------------
        # Return Signal
        # ---------------------------------

        signal = Signal(

            strategy="CRT",

            symbol=symbol,

            timeframe=timeframe,

            signal=True,

            direction=sweep.direction,

            entry=levels["entry"],

            stop_loss=levels["stop_loss"],

            take_profit=levels["take_profit"],

            confidence=1.0,

            reasons=[
                "HTF Range",
                "Liquidity Sweep",
                "Validation Passed",
                "BOS",
                "CHOCH",
                "MSS"
            ]

        )
        with open("logs/debug_signal.log", "a") as f:

            f.write("\n================ SIGNAL CONFIRMED ================\n")
            f.write(f"Confirmation Time : {entry_df.iloc[-1]['time']}\n")
            f.write(f"Direction         : {signal.direction}\n")
            f.write("\n")

            f.write("------------ SWEEP CANDLE ------------\n")
            f.write(f"Sweep Time        : {sweep.candle_time}\n")
            f.write(f"Sweep Open        : {sweep.open}\n")
            f.write(f"Sweep High        : {sweep.high}\n")
            f.write(f"Sweep Low         : {sweep.low}\n")
            f.write(f"Sweep Close       : {sweep.close}\n")
            f.write("\n")

            f.write("------------ TRADE LEVELS ------------\n")
            f.write(f"Entry             : {signal.entry}\n")
            f.write(f"Stop Loss         : {signal.stop_loss}\n")
            f.write(f"Take Profit       : {signal.take_profit}\n")
            f.write("===============================================\n")


            print("\n================ SIGNAL CONFIRMED ================")
            print(f"Confirmation Time : {entry_df.iloc[-1]['time']}")
            print(f"Direction         : {signal.direction}")

            print("\n------------ SWEEP CANDLE ------------")
            print(f"Sweep Time        : {sweep.candle_time}")
            print(f"Sweep Open        : {sweep.open}")
            print(f"Sweep High        : {sweep.high}")
            print(f"Sweep Low         : {sweep.low}")
            print(f"Sweep Close       : {sweep.close}")

            print("\n------------ TRADE LEVELS ------------")
            print(f"Entry             : {signal.entry}")
            print(f"Stop Loss         : {signal.stop_loss}")
            print(f"Take Profit       : {signal.take_profit}")
            print("==================================================\n")

            return signal