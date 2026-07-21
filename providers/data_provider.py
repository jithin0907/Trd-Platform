from providers.mt5_provider import MT5Provider

from indicators.ema import EMA
from indicators.sma import SMA


class DataProvider:
    """
    Provides market data enriched with technical indicators.
    """

    def __init__(self):

        self.mt5 = MT5Provider()

    def connect(self):

        return self.mt5.connect()

    def shutdown(self):

        self.mt5.shutdown()

    def get_market_data(
        self,
        symbol,
        timeframe="M15",
        bars=500
    ):

        # Get OHLC candles
        df = self.mt5.get_historical_data(
            symbol=symbol,
            timeframe=timeframe,
            bars=bars
        )

        # Add Moving Averages
        df["ema9"] = EMA.calculate(df, 9)

        df["ema20"] = EMA.calculate(df, 20)

        df["sma50"] = SMA.calculate(df, 50)

        return df