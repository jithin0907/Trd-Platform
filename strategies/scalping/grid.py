"""
====================================================
Scalping Grid Manager
====================================================
"""

from .config import ScalpingConfig


class GridManager:

    def __init__(self, trade_manager):

        self.trade_manager = trade_manager

    # =====================================================
    # CAN OPEN FIRST TRADE
    # =====================================================

    def can_open_first_trade(self):

        positions = self.trade_manager.get_positions()

        return len(positions) == 0

    # =====================================================
    # CAN ADD GRID ORDER
    # =====================================================

    def can_add_grid(self, current_price, signal):

        positions = self.trade_manager.get_positions()

        # --------------------------------------------
        # No positions
        # --------------------------------------------

        if len(positions) == 0:
            return True

        # --------------------------------------------
        # Maximum grid reached
        # --------------------------------------------

        if len(positions) >= ScalpingConfig.MAX_GRID_ORDERS:
            return False

        # --------------------------------------------
        # Last opened position
        # --------------------------------------------

        last_position = positions[-1]

        last_price = last_position.price_open

        spacing = ScalpingConfig.GRID_SPACING_PRICE

        # --------------------------------------------
        # BUY GRID
        # --------------------------------------------

        if signal == "BUY":

            if current_price <= (last_price - spacing):
                return True

        # --------------------------------------------
        # SELL GRID
        # --------------------------------------------

        elif signal == "SELL":

            if current_price >= (last_price + spacing):
                return True

        return False

    # =====================================================
    # GRID COUNT
    # =====================================================

    def grid_count(self):

        return len(self.trade_manager.get_positions())

    # =====================================================
    # GRID FULL
    # =====================================================

    def is_grid_full(self):

        return self.grid_count() >= ScalpingConfig.MAX_GRID_ORDERS

    # =====================================================
    # RESET
    # =====================================================

    def reset(self):

        # Reserved for future use
        pass