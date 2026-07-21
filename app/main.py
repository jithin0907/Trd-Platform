from config.settings import *

from backtesting.backtester import Backtester
from engine.live_engine import LiveEngine





def main():

    if MODE == BACKTEST:

        Backtester(
    strategy_name=STRATEGY,
    symbol=SYMBOL,
    timeframe=TIMEFRAME,
    bars=BARS,
    warmup=WARMUP
    ).run()

    elif MODE == LIVE:

        LiveEngine().run()

    else:

        raise Exception("Invalid MODE")


if __name__ == "__main__":
    main()