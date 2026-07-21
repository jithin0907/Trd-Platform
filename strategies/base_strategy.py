from abc import ABC, abstractmethod

from models.signal import Signal


class BaseStrategy(ABC):
    """
    Abstract base class for all trading strategies.
    Every strategy must implement the analyze() method.
    """

    @abstractmethod
    def analyze(
        self,
        symbol: str,
        timeframe: str,
        df
    ) -> Signal:
        """
        Analyze market data and return a Signal.

        Parameters
        ----------
        symbol : str
            Trading symbol (EURUSD, XAUUSD, etc.)

        timeframe : str
            Timeframe (M15, H1, etc.)

        df : pandas.DataFrame
            Market data with indicators.

        Returns
        -------
        Signal
            Standard trading signal.
        """
        pass