from strategies.ema_pullback.config import EMAConfig


class TradeLevels:
    """
    Calculates strategy-specific Stop Loss and Take Profit.
    """

    @staticmethod
    def calculate(df, direction, entry_price):

        candle = df.iloc[-1]

        sma50 = candle["sma50"]

        buffer = EMAConfig.SL_BUFFER_PIPS * 0.0001

        if direction == "BUY":

            stop_loss = sma50 - buffer

            risk = entry_price - stop_loss

            take_profit = entry_price + (
                risk * EMAConfig.RISK_REWARD
            )

        else:

            stop_loss = sma50 + buffer

            risk = stop_loss - entry_price

            take_profit = entry_price - (
                risk * EMAConfig.RISK_REWARD
            )

        return stop_loss, take_profit