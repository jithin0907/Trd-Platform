from strategies.base_strategy import BaseStrategy
from models.signal import Signal

from strategies.scalping.config import ScalpingConfig
from strategies.scalping.signal import (
    ScalpingSignalGenerator,
    SignalType
)
from strategies.scalping.trade import TradeManager
from strategies.scalping.grid import GridManager
from strategies.scalping.basket import BasketManager
from strategies.scalping.pause import PauseController


class ScalpingStrategy(BaseStrategy):

    def __init__(self):

        self.trade_manager = TradeManager()

        self.grid_manager = GridManager(
            self.trade_manager
        )

        self.basket_manager = BasketManager(
            self.trade_manager
        )

        self.pause_controller = PauseController()

        self.signal_generator = ScalpingSignalGenerator(
            ScalpingConfig
        )

    def analyze(
        self,
        symbol,
        timeframe,
        data
    ) -> Signal:

        # -----------------------------------------
        # Emergency Kill
        # -----------------------------------------

        if self.pause_controller.kill_requested():

            self.trade_manager.close_all()

            self.pause_controller.reset_kill()

            return Signal(
                strategy="SCALPING",
                symbol=symbol,
                timeframe=timeframe
            )

        # -----------------------------------------
        # Basket Monitoring
        # -----------------------------------------

        self.basket_manager.monitor()

        # -----------------------------------------
        # Pause Trading
        # -----------------------------------------

        if self.pause_controller.is_paused():

            return Signal(
                strategy="SCALPING",
                symbol=symbol,
                timeframe=timeframe
            )

        # -----------------------------------------
        # -----------------------------------------
        # -----------------------------------------
        # Entry Data
        # -----------------------------------------

        entry_df = data["entry"]

       
        # -----------------------------------------
        # Generate Signal
        # -----------------------------------------

        signal = self.signal_generator.generate_signal(entry_df)
        if signal == SignalType.NONE:

            return Signal(
                strategy="SCALPING",
                symbol=symbol,
                timeframe=timeframe
            )

       



        # -----------------------------------------
        # Current Market Price
        # -----------------------------------------

        current_price = entry_df.iloc[-1]["close"]

        # -----------------------------------------
        # First Trade
        # -----------------------------------------

        if self.grid_manager.can_open_first_trade():

            if signal == SignalType.BUY:
                self.trade_manager.buy()

            else:
                self.trade_manager.sell()

        # -----------------------------------------
        # Grid Layer
        # -----------------------------------------

        else:

            if self.grid_manager.can_add_grid(
                current_price,
                signal.value
            ):

                if signal == SignalType.BUY:
                    self.trade_manager.buy()

                else:
                    self.trade_manager.sell()

        # -----------------------------------------
        # Return Platform Signal
        # -----------------------------------------

        # -----------------------------------------
        # Calculate SL / TP
        # -----------------------------------------

        if signal == SignalType.BUY:

            stop_loss = current_price - 0.30
            take_profit = current_price + 0.60

        else:

            stop_loss = current_price + 0.30
            take_profit = current_price - 0.60

        # -----------------------------------------
        # Return Platform Signal
        # -----------------------------------------

        return Signal(

            strategy="SCALPING",

            symbol=symbol,

            timeframe=timeframe,

            signal=True,

            direction=signal.value,

            entry=current_price,

            stop_loss=stop_loss,

            take_profit=take_profit,

            confidence=1.0,

            reasons=[
                "Scalping Signal",
                "Grid Manager",
                "Basket Manager"
            ]

        )