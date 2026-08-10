"""
====================================================
Scalping Signal Generator
====================================================
"""

from enum import Enum


class SignalType(Enum):
    BUY = "BUY"
    SELL = "SELL"
    NONE = "NONE"


class ScalpingSignalGenerator:

    def __init__(self, config):
        self.config = config

    def generate_signal(self, market_data):
        """
        Returns:
            SignalType.BUY
            SignalType.SELL
            SignalType.NONE
        """

        # -------------------------------------------------
        # Make sure enough candles exist
        # -------------------------------------------------

        if len(market_data) < 50:
            return SignalType.NONE

        # -------------------------------------------------
        # Calculate EMA20
        # -------------------------------------------------

        ema20 = market_data["close"].ewm(span=20).mean()

        # -------------------------------------------------
        # Calculate EMA50
        # -------------------------------------------------

        ema50 = market_data["close"].ewm(span=50).mean()

        # -------------------------------------------------
        # Latest Candle
        # -------------------------------------------------

        current_close = market_data["close"].iloc[-1]

        current_open = market_data["open"].iloc[-1]



        # -------------------------------------------------
        # Trend
        # -------------------------------------------------

        bullish = ema20.iloc[-1] > ema50.iloc[-1]

        bearish = ema20.iloc[-1] < ema50.iloc[-1]

        # -------------------------------------------------
        # BUY
        # -------------------------------------------------

        # -------------------------------------------------
        # Previous Candle
        # -------------------------------------------------

        previous_close = market_data["close"].iloc[-2]
        previous_open = market_data["open"].iloc[-2]
        previous_low = market_data["low"].iloc[-2]
        previous_high = market_data["high"].iloc[-2]

        # -------------------------------------------------
        # EMA Direction
        # -------------------------------------------------

        ema20_current = ema20.iloc[-1]
        ema20_previous = ema20.iloc[-2]

        ema50_current = ema50.iloc[-1]
        ema50_previous = ema50.iloc[-2]

        ema20_up = ema20_current > ema20_previous
        ema50_up = ema50_current > ema50_previous

        ema20_down = ema20_current < ema20_previous
        ema50_down = ema50_current < ema50_previous

        # -------------------------------------------------
        # Session Filter
        # -------------------------------------------------

        hour = market_data.iloc[-1]["time"].hour

        if hour < 8 or hour > 20:
            return SignalType.NONE

        # -------------------------------------------------
        # BUY
        # -------------------------------------------------

        if (
            bullish
            and ema20_up
            and ema50_up
            and previous_low <= ema20_previous
            and current_close > previous_close
            and current_close > current_open
            
        ):

            return SignalType.BUY

        # -------------------------------------------------
        # SELL
        # -------------------------------------------------

        if (
            bearish
            and ema20_down
            and ema50_down
            and previous_high >= ema20_previous
            and current_close < previous_close
            and current_close < current_open
            
        ):

            return SignalType.SELL

        return SignalType.NONE
      