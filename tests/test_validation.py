from providers.mt5_provider import MT5Provider
from config.settings import SYMBOL

symbol = SYMBOL

from strategies.crt.config import (
    HTF_TIMEFRAME,
    ENTRY_TIMEFRAME,
    HTF_BARS
)

from strategies.crt.htf_range import HTFRangeDetector
from strategies.crt.sweep_detector import SweepDetector
from strategies.crt.validation import Validation


def main():

    provider = MT5Provider()

    if not provider.connect():
        return

   

    # -----------------------------------
    # HTF Data
    # -----------------------------------

    htf_df = provider.get_historical_data(
        symbol=symbol,
        timeframe=HTF_TIMEFRAME,
        bars=HTF_BARS
    )

    htf_range = HTFRangeDetector.get(htf_df)

    # -----------------------------------
    # Entry Timeframe Data
    # -----------------------------------

    entry_df = provider.get_historical_data(
        symbol=symbol,
        timeframe=ENTRY_TIMEFRAME,
        bars=300
    )

    # -----------------------------------
    # Detect Sweep
    # -----------------------------------

    sweep = SweepDetector.detect(
        entry_df,
        htf_range
    )

    print("\n========== VALIDATION ==========\n")

    if sweep is None:

        print("No Sweep Found")

    else:

        print(sweep)

        valid = Validation.validate(
            sweep,
            htf_range
        )

        print("--------------------------------")
        print("CRT VALID :", valid)
        print("--------------------------------")

    provider.shutdown()


if __name__ == "__main__":
    main()