"""
Higher Timeframe Range Detector

Responsible for:

- Selecting the latest CLOSED HTF candle
- Returning its High
- Returning its Low
- Returning its Open
- Returning its Close
"""

from dataclasses import dataclass


@dataclass
class HTFRange:

    time: object
    open: float
    high: float
    low: float
    close: float

    @property
    def range(self):
        return self.high - self.low

    @property
    def mid(self):
        return (self.high + self.low) / 2


class HTFRangeDetector:

    @staticmethod
    def get(df):

        if df is None or len(df) < 2:
            return None

        # Last candle may still be forming.
        # Use the previous candle.
        candle = df.iloc[-2]

        return HTFRange(
            time=candle["time"],
            open=float(candle["open"]),
            high=float(candle["high"]),
            low=float(candle["low"]),
            close=float(candle["close"])
        )