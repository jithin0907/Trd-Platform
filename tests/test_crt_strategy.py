from providers.mt5_provider import MT5Provider

from config.settings import SYMBOL

from strategies.crt.config import (
    HTF_TIMEFRAME,
    ENTRY_TIMEFRAME,
    HTF_BARS
)

from strategies.crt.strategy import CRTStrategy


def main():

    provider = MT5Provider()

    if not provider.connect():
        return

    # -----------------------------------
    # Download HTF Data
    # -----------------------------------

    htf_df = provider.get_historical_data(
        symbol=SYMBOL,
        timeframe=HTF_TIMEFRAME,
        bars=HTF_BARS
    )

    # -----------------------------------
    # Download Entry Data
    # -----------------------------------

    entry_df = provider.get_historical_data(
        symbol=SYMBOL,
        timeframe=ENTRY_TIMEFRAME,
        bars=300
    )

    # -----------------------------------
    # Package Data
    # -----------------------------------

    data = {

        "htf": htf_df,

        "entry": entry_df

    }

    # -----------------------------------
    # Analyze
    # -----------------------------------

    strategy = CRTStrategy()

    signal = strategy.analyze(

        symbol=SYMBOL,

        timeframe=ENTRY_TIMEFRAME,

        data=data

    )

    # -----------------------------------
    # Print Result
    # -----------------------------------

    print("\n========== CRT SIGNAL ==========\n")

    print("Strategy      :", signal.strategy)
    print("Symbol        :", signal.symbol)
    print("Timeframe     :", signal.timeframe)
    print("Signal        :", signal.signal)
    print("Direction     :", signal.direction)
    print("Entry         :", signal.entry)
    print("Stop Loss     :", signal.stop_loss)
    print("Take Profit   :", signal.take_profit)
    print("Confidence    :", signal.confidence)

    print("\nReasons")

    for reason in signal.reasons:

        print("-", reason)

    provider.shutdown()


if __name__ == "__main__":
    main()