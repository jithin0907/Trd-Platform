import MetaTrader5 as mt5


class SymbolInfo:

    @staticmethod
    def get(symbol: str):
        """
        Returns MT5 symbol information as a dictionary.

        Raises:
            Exception if symbol is not available.
        """

        info = mt5.symbol_info(symbol)

        if info is None:
            raise Exception(f"Unable to get symbol information for {symbol}")

        return {
            "symbol": info.name,
            "digits": info.digits,
            "point": info.point,
            "tick_size": info.trade_tick_size,
            "tick_value": info.trade_tick_value,
            "contract_size": info.trade_contract_size,
            "volume_min": info.volume_min,
            "volume_max": info.volume_max,
            "volume_step": info.volume_step,
            "spread": info.spread,
        }