from providers.mt5_provider import MT5Provider

from strategies.crt.config import (
    HTF_TIMEFRAME,
    ENTRY_TIMEFRAME,
    HTF_BARS
)

from strategies.crt.htf_range import HTFRangeDetector
from strategies.crt.sweep_detector import SweepDetector


def main():

    provider = MT5Provider()

    if not provider.connect():
        return

    symbol = "EURUSD"

    # -----------------------------------
    # Get HTF Data
    # -----------------------------------

    htf_df = provider.get_historical_data(
        symbol=symbol,
        timeframe=HTF_TIMEFRAME,
        bars=HTF_BARS
    )

    htf_range = HTFRangeDetector.get(htf_df)

    print("\n========== HTF RANGE ==========")

    print("Time  :", htf_range.time)
    print("High  :", htf_range.high)
    print("Low   :", htf_range.low)

    # -----------------------------------
    # Get Entry Timeframe Data
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

    print("\n========== SWEEP ==========")

    if sweep is None:

        print("No Sweep Found")

    else:

        print(sweep)

    provider.shutdown()


if __name__ == "__main__":
    main()