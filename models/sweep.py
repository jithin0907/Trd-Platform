from dataclasses import dataclass
from datetime import datetime


@dataclass
class Sweep:
    """
    Represents a detected liquidity sweep.
    """

    valid: bool

    # BUY or SELL
    direction: str

    # Price that swept liquidity
    sweep_price: float

    # HTF level that was swept
    htf_level: float

    # Index of the candle in the entry timeframe
    candle_index: int

    # Candle timestamp
    candle_time: datetime

    # OHLC of the sweep candle
    open: float
    high: float
    low: float
    close: float

    @property
    def sweep_distance(self):
        """
        Distance between the sweep price and the HTF level.
        """
        return abs(self.sweep_price - self.htf_level)

    def __str__(self):

        return (
            f"\n========== SWEEP ==========\n"
            f"Valid      : {self.valid}\n"
            f"Direction  : {self.direction}\n"
            f"Time       : {self.candle_time}\n"
            f"HTF Level  : {self.htf_level}\n"
            f"SweepPrice : {self.sweep_price}\n"
            f"Distance   : {self.sweep_distance:.5f}\n"
            f"OHLC       : "
            f"{self.open} "
            f"{self.high} "
            f"{self.low} "
            f"{self.close}\n"
        )