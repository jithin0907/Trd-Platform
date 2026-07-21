import pandas as pd


class EMA:

    @staticmethod
    def calculate(df: pd.DataFrame, period: int, column: str = "close"):

        ema = df[column].ewm(
            span=period,
            adjust=False
        ).mean()

        return ema