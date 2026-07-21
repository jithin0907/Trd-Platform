from strategies.ema_pullback.config import EMAConfig


class TrendDetector:

    @staticmethod
    def detect(df):

        if len(df) < EMAConfig.SMA_TREND:
            return None

        current = df.iloc[-1]
        previous = df.iloc[-2]

        # Current values
        ema9 = current["ema9"]
        ema20 = current["ema20"]
        sma50 = current["sma50"]

        # Previous values (used for slope)
        prev_ema9 = previous["ema9"]
        prev_ema20 = previous["ema20"]
        prev_sma50 = previous["sma50"]

        bullish_alignment = (
            ema9 > ema20 > sma50
        )

        bearish_alignment = (
            ema9 < ema20 < sma50
        )

        bullish_slope = (
            ema9 > prev_ema9 and
            ema20 > prev_ema20 and
            sma50 > prev_sma50
        )

        bearish_slope = (
            ema9 < prev_ema9 and
            ema20 < prev_ema20 and
            sma50 < prev_sma50
        )

        if bullish_alignment and bullish_slope:
            return "BUY"

        if bearish_alignment and bearish_slope:
            return "SELL"

        return None