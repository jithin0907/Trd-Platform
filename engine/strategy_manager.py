from strategies.ema_pullback.strategy import EMAPullbackStrategy
from strategies.crt.strategy import CRTStrategy



class StrategyManager:
    """
    Loads and manages trading strategies.
    """

    _strategies = {}

    @classmethod
    def register(cls, name: str, strategy_class):
        cls._strategies[name] = strategy_class

    @classmethod
    def load(cls, name: str):

        if name not in cls._strategies:
            raise ValueError(f"Strategy '{name}' not found.")

        return cls._strategies[name]()

    @classmethod
    def list_strategies(cls):
        return list(cls._strategies.keys())


# Register built-in strategies
StrategyManager.register(
    "ema_pullback",
    EMAPullbackStrategy
)

StrategyManager.register(
    "crt",
    CRTStrategy
)