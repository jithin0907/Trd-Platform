from strategies.ema_pullback.config import EMAConfig


class PullbackDetector:
    """
    Detects pullbacks to the 20 EMA.
    """

    @staticmethod
    def bullish(df):

        candle = df.iloc[-1]

        ema20 = candle["ema20"]

        return (
            candle["low"] <= ema20 + EMAConfig.TOUCH_TOLERANCE
            and
            candle["close"] >= ema20
        )

    @staticmethod
    def bearish(df):

        candle = df.iloc[-1]

        ema20 = candle["ema20"]

        return (
            candle["high"] >= ema20 - EMAConfig.TOUCH_TOLERANCE
            and
            candle["close"] <= ema20
        )