"""
====================================================
Scalping Basket Manager
====================================================
"""

from .config import ScalpingConfig


class BasketManager:

    def __init__(self, trade_manager):

        self.trade_manager = trade_manager

    # =====================================================
    # TOTAL BASKET PROFIT
    # =====================================================

    def get_total_profit(self):

        return self.trade_manager.basket_profit()

    # =====================================================
    # TARGET REACHED
    # =====================================================

    def target_reached(self):

        profit = self.get_total_profit()

        return profit >= ScalpingConfig.TARGET_PROFIT_USD

    # =====================================================
    # CLOSE BASKET
    # =====================================================

    def close_basket(self):

        self.trade_manager.close_all()

    # =====================================================
    # MONITOR
    # =====================================================

    def monitor(self):

        if self.target_reached():

            print(
                f"[Basket] Target reached : "
                f"${self.get_total_profit():.2f}"
            )

            self.close_basket()

            return True

        return False

    # =====================================================
    # BASKET STATUS
    # =====================================================

    def basket_status(self):

        positions = self.trade_manager.get_positions()

        return {
            "positions": len(positions),
            "profit": self.get_total_profit(),
            "target": ScalpingConfig.TARGET_PROFIT_USD
        }