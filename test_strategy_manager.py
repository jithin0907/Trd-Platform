from engine.strategy_manager import StrategyManager
from strategies.base_strategy import BaseStrategy


class DummyStrategy(BaseStrategy):

    def analyze(self, market_data):
        print("Dummy Strategy Running")


StrategyManager.register("dummy", DummyStrategy)

strategy = StrategyManager.load("dummy")

strategy.analyze(None)

print()

print("Available Strategies:")

print(StrategyManager.list_strategies())