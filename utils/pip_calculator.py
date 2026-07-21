from utils.symbol_info import SymbolInfo


class PipCalculator:

    @staticmethod
    def get_pip_size(symbol: str):
        """
        Returns the pip size for the given symbol.
        """

        info = SymbolInfo.get(symbol)

        digits = info["digits"]
        point = info["point"]

        # Forex pairs with 5 or 3 decimal digits
        if digits == 5:
            return point * 10

        if digits == 3:
            return point * 10

        # Forex pairs with 4 or 2 decimal digits
        if digits == 4:
            return point

        if digits == 2:
            return point

        # Gold, Crypto, Indices and other symbols
        # Fallback to broker's minimum price movement
        tick_size = info["tick_size"]

        if tick_size > 0:
            return tick_size

        return point

    @staticmethod
    def calculate(symbol: str, entry: float, exit: float):
        """
        Returns profit/loss in pips.
        Positive = Profit
        Negative = Loss
        """

        pip_size = PipCalculator.get_pip_size(symbol)

        return (exit - entry) / pip_size
    
    @staticmethod
    def pips_to_price(symbol: str, pips: float):
        """
        Converts pips/points into a price movement.

        Examples
        --------
        EURUSD
            5 pips -> 0.00050

        XAUUSD
            5 points -> 0.50

        XAGUSD
            5 points -> 0.05
        """

        pip_size = PipCalculator.get_pip_size(symbol)

        return pip_size * pips   