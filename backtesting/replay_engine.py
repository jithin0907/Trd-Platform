import pandas as pd


class ReplayEngine:
    """
    Replays historical market data candle by candle.
    Supports jumping to any candle (used after a trade closes).
    """

    def __init__(self, df: pd.DataFrame, warmup: int = 100):

        self.df = df
        self.warmup = warmup
        self.position = warmup

    def has_next(self):
        """
        Returns True if there are more candles.
        """
        return self.position < len(self.df)

    def next(self):
        """
        Returns the next candle and advances the replay.
        """

        index = self.position

        market = self.df.iloc[:index + 1].copy()

        self.position += 1

        return index, market

    def jump_to(self, index):
        """
        Jump replay to a specific candle.
        Used after a trade closes.
        """

        self.position = max(index, self.position)

    def reset(self):
        self.position = self.warmup
        """
        Restart replay from the warmup candle.
        """

        self.position = self.warmup

    def replay(self):
     """
     Backward compatible replay generator.
     """

     while self.has_next():
        yield self.next()