"""
====================================================
Scalping Trade Manager
====================================================
"""

import MetaTrader5 as mt5

from .config import ScalpingConfig


class TradeManager:

    def __init__(self):

        self.symbol = ScalpingConfig.SYMBOL
        self.magic = ScalpingConfig.MAGIC_NUMBER
        self.volume = ScalpingConfig.BASE_LOT_SIZE

    # =====================================================
    # BUY
    # =====================================================

    def buy(self):

        tick = mt5.symbol_info_tick(self.symbol)

        if tick is None:
            return None

        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": self.symbol,
            "volume": self.volume,
            "type": mt5.ORDER_TYPE_BUY,
            "price": tick.ask,
            "magic": self.magic,
            "deviation": ScalpingConfig.MAX_SLIPPAGE,
            "comment": "Scalping BUY",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }

        return mt5.order_send(request)

    # =====================================================
    # SELL
    # =====================================================

    def sell(self):

        tick = mt5.symbol_info_tick(self.symbol)

        if tick is None:
            return None

        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": self.symbol,
            "volume": self.volume,
            "type": mt5.ORDER_TYPE_SELL,
            "price": tick.bid,
            "magic": self.magic,
            "deviation": ScalpingConfig.MAX_SLIPPAGE,
            "comment": "Scalping SELL",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }

        return mt5.order_send(request)

    # =====================================================
    # OPEN POSITIONS
    # =====================================================

    def get_positions(self):

        positions = mt5.positions_get(symbol=self.symbol)

        if positions is None:
            return []

        return [
            p for p in positions
            if p.magic == self.magic
        ]

    # =====================================================
    # TOTAL BASKET PROFIT
    # =====================================================

    def basket_profit(self):

        positions = self.get_positions()

        total = 0.0

        for position in positions:
            total += position.profit

        return total

    # =====================================================
    # CLOSE POSITION
    # =====================================================

    def close_position(self, position):

        tick = mt5.symbol_info_tick(self.symbol)

        if tick is None:
            return None

        order_type = (
            mt5.ORDER_TYPE_SELL
            if position.type == mt5.POSITION_TYPE_BUY
            else mt5.ORDER_TYPE_BUY
        )

        price = (
            tick.bid
            if position.type == mt5.POSITION_TYPE_BUY
            else tick.ask
        )

        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": self.symbol,
            "volume": position.volume,
            "type": order_type,
            "position": position.ticket,
            "price": price,
            "magic": self.magic,
            "deviation": ScalpingConfig.MAX_SLIPPAGE,
            "comment": "Scalping Close",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }

        return mt5.order_send(request)

    # =====================================================
    # CLOSE ALL
    # =====================================================

    def close_all(self):

        positions = self.get_positions()

        for position in positions:
            self.close_position(position)