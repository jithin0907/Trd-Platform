from strategies.base_strategy import BaseStrategy

from models.signal import Signal

from strategies.crt.htf_range import HTFRangeDetector
from strategies.crt.sweep_detector import SweepDetector
from strategies.crt.validation import Validation
from strategies.crt.trade_levels import TradeLevels
from engine.market_structure_engine import MarketStructureEngine


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

        # ---------------------------------
        # Return Signal
        # ---------------------------------

        return Signal(

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