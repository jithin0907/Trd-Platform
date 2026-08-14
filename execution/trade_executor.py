import MetaTrader5 as mt5
from datetime import datetime

from config.settings import *


class TradeExecutor:

    def __init__(self):
        pass

    # ----------------------------------------
    # Place Trade
    # ----------------------------------------

    print("\n" + "=" * 60)
    print("CUSTOM TRADE EXECUTOR IS RUNNING")
    print("=" * 60)

    def place_trade(self, signal):

        symbol = signal.symbol

        # ----------------------------------------
        # One Trade Per Symbol
        # ----------------------------------------

        if ONE_TRADE_PER_SYMBOL:

            positions = mt5.positions_get(symbol=symbol)

            if positions is None:

                print("Unable to check open positions.")
                print(mt5.last_error())

                return None

            if len(positions) > 0:

                print()
                print("=" * 60)
                print(f"{symbol} already has an open position.")
                print("Skipping trade...")
                print("=" * 60)

                return None        

        # Ensure symbol is available
        if not mt5.symbol_select(symbol, True):
            print(f"Unable to select {symbol}")
            return None

        # Get latest market price
        tick = mt5.symbol_info_tick(symbol)

        if tick is None:
            print("Unable to get market tick.")
            return None

        # ----------------------------------------
        # Determine Order Type
        # ----------------------------------------

        current_price = tick.ask if signal.direction == "BUY" else tick.bid

        entry_difference = abs(current_price - signal.entry)

        print("\n" + "=" * 60)
        print("ENTRY CHECK")
        print("=" * 60)
        print(f"Signal Entry     : {signal.entry}")
        print(f"Current Price    : {current_price}")
        print(f"Difference       : {round(entry_difference, 3)}")
        print(f"Allowed          : {MAX_ENTRY_DEVIATION}")

        if signal.direction == "BUY":

            if entry_difference <= MAX_ENTRY_DEVIATION:

                print("Using MARKET BUY")

                order_type = mt5.ORDER_TYPE_BUY
                action = mt5.TRADE_ACTION_DEAL
                price = current_price

            else:

                print("Using BUY LIMIT")

                order_type = mt5.ORDER_TYPE_BUY_LIMIT
                action = mt5.TRADE_ACTION_PENDING
                price = signal.entry

        elif signal.direction == "SELL":

            if entry_difference <= MAX_ENTRY_DEVIATION:

                print("Using MARKET SELL")

                order_type = mt5.ORDER_TYPE_SELL
                action = mt5.TRADE_ACTION_DEAL
                price = current_price

            else:

                print("Using SELL LIMIT")

                order_type = mt5.ORDER_TYPE_SELL_LIMIT
                action = mt5.TRADE_ACTION_PENDING
                price = signal.entry

        else:

            print("Invalid trade direction.")
            return None

        print("=" * 60)

# ----------------------------------------
        # Validate Pending Order Price
        # ----------------------------------------

        if order_type == mt5.ORDER_TYPE_BUY_LIMIT:

            if price >= current_price:

                print("=" * 60)
                print("LIMIT ORDER VALIDATION FAILED")
                print(f"Current Price : {current_price}")
                print(f"Order Price   : {price}")
                print(f"Order Type    : {order_type}")
                print("=" * 60)
                return None
                

        elif order_type == mt5.ORDER_TYPE_SELL_LIMIT:

            if price <= current_price:

                print("=" * 60)
                print("LIMIT ORDER VALIDATION FAILED")
                print(f"Current Price : {current_price}")
                print(f"Order Price   : {price}")
                print(f"Order Type    : {order_type}")
                print("=" * 60)
                return None  


        

        # Build order request
        request = {

            "action": action,

            "symbol": symbol,

            "volume": LOT_SIZE,

            "type": order_type,

            "price": price,

            "sl": signal.stop_loss,

            "tp": signal.take_profit,

            "deviation": 20,

            "magic": MAGIC_NUMBER,

            "comment": STRATEGY,

            "type_time": mt5.ORDER_TIME_GTC,

            "type_filling": mt5.ORDER_FILLING_FOK

        }

        # ----------------------------------------
        # Debug Order Request
        # ----------------------------------------

        print("\n" + "=" * 60)
        print("ORDER REQUEST")
        print("=" * 60)

        print(f"Order Time     : {datetime.now()}")
        print(f"Direction      : {signal.direction}")
        print(f"Signal Entry   : {signal.entry}")
        print(f"Current Price  : {current_price}")
        print(f"Order Price    : {price}")
        print(f"Order Type     : {order_type}")
        print(f"Stop Loss      : {signal.stop_loss}")
        print(f"Take Profit    : {signal.take_profit}")

        risk = abs(signal.entry - signal.stop_loss)
        reward = abs(signal.take_profit - signal.entry)

        if risk != 0:
            rr = reward / risk
        else:
            rr = 0

        print(f"Risk           : {risk}")
        print(f"Reward         : {reward}")
        print(f"Calculated RR  : {round(rr, 2)}")

        print("=" * 60)


        print("\nREQUEST SENT TO MT5")
        print("=" * 60)

        for key, value in request.items():
            print(f"{key:15}: {value}")

        print("=" * 60)


        with open("logs/trade_execution_log.txt", "a") as f:
         f.write("\n================ ORDER REQUEST ================\n")
         f.write(f"Order Time     : {datetime.now()}\n")
         f.write(f"Direction      : {signal.direction}\n")
         f.write(f"Signal Entry   : {signal.entry}\n")
         f.write(f"Current Price  : {current_price}\n")
         f.write(f"Order Price    : {price}\n")
         f.write(f"Order Type     : {order_type}\n")
         f.write(f"Stop Loss      : {signal.stop_loss}\n")
         f.write(f"Take Profit    : {signal.take_profit}\n")
         f.write(f"Risk           : {risk}\n")
         f.write(f"Reward         : {reward}\n")
         f.write(f"Calculated RR  : {round(rr, 2)}\n")
         f.write("===============================================\n")

        # ----------------------------------------
        # Send Order
        # ----------------------------------------
        print("About to send order...")
        result = mt5.order_send(request)
        
        print("Order sent.")
        print(result)

        # Check result
        if result is None:

            print("MT5 returned None.")
            print(mt5.last_error())

            return None


        with open("logs/trade_execution_log.txt", "a") as f:
            f.write("\nMT5 RESPONSE\n")
            f.write(f"RetCode        : {result.retcode}\n")

            if result.retcode in (
                mt5.TRADE_RETCODE_DONE,
                mt5.TRADE_RETCODE_PLACED
            ):
                f.write(f"Order Ticket   : {result.order}\n")
                f.write(f"Deal Ticket    : {result.deal}\n")

                if result.retcode == mt5.TRADE_RETCODE_PLACED:
                    f.write("Status         : PENDING ORDER PLACED\n")
                else:
                    f.write("Status         : SUCCESS\n")

            else:
                f.write("Status         : FAILED\n")
                f.write(f"Result         : {result}\n")

            f.write("=" * 70 + "\n")

        

        

        

        if result.retcode not in (
            mt5.TRADE_RETCODE_DONE,
            mt5.TRADE_RETCODE_PLACED
        ):

            print("Trade Failed")
            print("RetCode :", result.retcode)
            print(result)

            return result

        # Success
        print()
        print("=" * 60)

        if result.retcode == mt5.TRADE_RETCODE_PLACED:

            print("PENDING ORDER PLACED")

        else:

            print("TRADE EXECUTED")

        print("=" * 60)
        print(f"Ticket    : {result.order}")
        print(f"Symbol    : {symbol}")
        print(f"Direction : {signal.direction}")
        print(f"Entry     : {price}")
        print(f"SL        : {signal.stop_loss}")
        print(f"TP        : {signal.take_profit}")
        print("=" * 60)

        return result

    def cancel_pending_orders(self, symbol):

        orders = mt5.orders_get()

        if orders is None:
            return

        for order in orders:

            # Only this EA's orders
            if order.magic != MAGIC_NUMBER:
                continue

            # Only cancel orders for this symbol
            if order.symbol != symbol:
                continue

            # Cancel only LIMIT pending orders
            if order.type not in (
                mt5.ORDER_TYPE_BUY_LIMIT,
                mt5.ORDER_TYPE_SELL_LIMIT
            ):
                continue

            request = {

                "action": mt5.TRADE_ACTION_REMOVE,
                "order": order.ticket

            }

            result = mt5.order_send(request)

            if result.retcode == mt5.TRADE_RETCODE_DONE:

                print(
                    f"Pending Order Cancelled : "
                    f"{symbol} : {order.ticket}"
                )

            else:

                print(
                    f"Failed to Cancel : "
                    f"{symbol} : {order.ticket}"
                )