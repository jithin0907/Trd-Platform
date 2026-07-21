import MetaTrader5 as mt5

from config.settings import *


class TradeExecutor:

    def __init__(self):
        pass

    # ----------------------------------------
    # Place Trade
    # ----------------------------------------

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

        # Determine order type
        if signal.direction == "BUY":

            order_type = mt5.ORDER_TYPE_BUY
            price = tick.ask

        elif signal.direction == "SELL":

            order_type = mt5.ORDER_TYPE_SELL
            price = tick.bid

        else:

            print("Invalid trade direction.")
            return None

        # Build order request
        request = {

            "action": mt5.TRADE_ACTION_DEAL,

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

            "type_filling": mt5.ORDER_FILLING_IOC

        }

        # ----------------------------------------
        # Debug Order Request
        # ----------------------------------------

        print("\n" + "=" * 60)
        print("ORDER REQUEST")
        print("=" * 60)

        print(f"Direction      : {signal.direction}")
        print(f"Signal Entry   : {signal.entry}")
        print(f"Market Price   : {price}")
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

        # ----------------------------------------
        # Send Order
        # ----------------------------------------

        result = mt5.order_send(request)

        # Check result
        if result is None:

            print("MT5 returned None.")
            print(mt5.last_error())

            return None


        with open("logs/trade_execution_log.txt", "a") as f:
            f.write("\nMT5 RESPONSE\n")
            f.write(f"RetCode        : {result.retcode}\n")

            if result.retcode == mt5.TRADE_RETCODE_DONE:
                f.write(f"Order Ticket   : {result.order}\n")
                f.write(f"Deal Ticket    : {result.deal}\n")
                f.write("Status         : SUCCESS\n")
            else:
                f.write("Status         : FAILED\n")
                f.write(f"Result         : {result}\n")

            f.write("=" * 70 + "\n")

        

        

        

        if result.retcode != mt5.TRADE_RETCODE_DONE:

            print("Trade Failed")
            print("RetCode :", result.retcode)
            print(result)

            return result

        # Success
        print()
        print("=" * 60)
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