import pandas as pd


class SMA:

    @staticmethod
    def calculate(df: pd.DataFrame, period: int, column: str = "close"):

        sma = df[column].rolling(
            window=period
        ).mean()

        return sma