from models.signal import Signal

from strategies.base_strategy import BaseStrategy

from strategies.ema_pullback.trend import TrendDetector
from strategies.ema_pullback.pullback import PullbackDetector
from strategies.ema_pullback.confirmation import ConfirmationDetector
from strategies.ema_pullback.trade_levels import TradeLevels


class EMAPullbackStrategy(BaseStrategy):
    """
    EMA Pullback Strategy
    """

    def analyze(
        self,
        symbol,
        timeframe,
        df
    ) -> Signal:

        trend = TrendDetector.detect(df)

        if trend is None:

            return Signal(
                strategy="EMA Pullback",
                symbol=symbol,
                timeframe=timeframe,
                signal=False
            )

        candle = df.iloc[-1]
        entry_price = candle["close"]

        # ===========================
        # BUY
        # ===========================

        if trend == "BUY":

            if not PullbackDetector.bullish(df):
                return Signal(
                    strategy="EMA Pullback",
                    symbol=symbol,
                    timeframe=timeframe,
                    signal=False
                )

            if not ConfirmationDetector.bullish(df):
                return Signal(
                    strategy="EMA Pullback",
                    symbol=symbol,
                    timeframe=timeframe,
                    signal=False
                )

            stop_loss, take_profit = TradeLevels.calculate(
                df,
                "BUY",
                entry_price
            )

            return Signal(
                strategy="EMA Pullback",
                symbol=symbol,
                timeframe=timeframe,
                signal=True,
                direction="BUY",
                entry=entry_price,
                stop_loss=stop_loss,
                take_profit=take_profit,
                confidence=85,
                reasons=[
                    "Bullish Trend",
                    "20 EMA Pullback",
                    "Bullish Confirmation"
                ]
            )

        # ===========================
        # SELL
        # ===========================

        if trend == "SELL":

            if not PullbackDetector.bearish(df):
                return Signal(
                    strategy="EMA Pullback",
                    symbol=symbol,
                    timeframe=timeframe,
                    signal=False
                )

            if not ConfirmationDetector.bearish(df):
                return Signal(
                    strategy="EMA Pullback",
                    symbol=symbol,
                    timeframe=timeframe,
                    signal=False
                )

            stop_loss, take_profit = TradeLevels.calculate(
                df,
                "SELL",
                entry_price
            )

            return Signal(
                strategy="EMA Pullback",
                symbol=symbol,
                timeframe=timeframe,
                signal=True,
                direction="SELL",
                entry=entry_price,
                stop_loss=stop_loss,
                take_profit=take_profit,
                confidence=85,
                reasons=[
                    "Bearish Trend",
                    "20 EMA Pullback",
                    "Bearish Confirmation"
                ]
            )

        return Signal(
            strategy="EMA Pullback",
            symbol=symbol,
            timeframe=timeframe,
            signal=False
        )