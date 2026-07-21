class ConfirmationDetector:
    """
    Detects confirmation candles for the EMA Pullback strategy.
    """

    @staticmethod
    def bullish(df):
        """
        Returns True if the latest candle is bullish.
        """

        candle = df.iloc[-1]

        return candle["close"] > candle["open"]

    @staticmethod
    def bearish(df):
        """
        Returns True if the latest candle is bearish.
        """

        candle = df.iloc[-1]

        return candle["close"] < candle["open"]