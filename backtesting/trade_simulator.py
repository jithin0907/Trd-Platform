from utils.pip_calculator import PipCalculator

class TradeSimulator:
    """
    Simulates an open trade until Stop Loss or Take Profit is hit.
    Also calculates trade statistics such as profit, RR and duration.
    """

    @staticmethod
    def simulate(df, start_index, signal):

        direction = signal.direction

        entry = signal.entry
        sl = signal.stop_loss
        tp = signal.take_profit

        # ----------------------------------
        # Trade Statistics
        # ----------------------------------

        risk = abs(entry - sl)
        reward = abs(tp - entry)

        # ----------------------------------
        # Scan future candles
        # ----------------------------------

        for i in range(start_index + 1, len(df)):

            candle = df.iloc[i]

            high = candle["high"]
            low = candle["low"]

            # ==========================================
            # BUY TRADE
            # ==========================================

            if direction == "BUY":

                # Stop Loss Hit
                if low <= sl:

                    profit = sl - entry
                    duration = i - start_index

                    return {

                        "result": "LOSS",

                        "entry_index": start_index,
                        "exit_index": i,

                        "entry_time": df.iloc[start_index]["time"],
                        "exit_time": df.iloc[i]["time"],

                        "entry_price": entry,
                        "exit_price": sl,

                        "stop_loss": sl,
                        "take_profit": tp,

                        "profit": profit,
                        "profit_pips": PipCalculator.calculate(
                        signal.symbol,
                         entry,
                         sl
                    ),

                        "risk": risk,
                        "reward": reward,

                        "rr": reward / risk if risk > 0 else 0,

                        "duration": duration

                    }

                # Take Profit Hit
                if high >= tp:

                    profit = tp - entry
                    duration = i - start_index

                    return {

                        "result": "WIN",

                        "entry_index": start_index,
                        "exit_index": i,

                        "entry_time": df.iloc[start_index]["time"],
                        "exit_time": df.iloc[i]["time"],

                        "entry_price": entry,
                        "exit_price": tp,

                        "stop_loss": sl,
                        "take_profit": tp,

                        "profit": profit,
                        "profit_pips": PipCalculator.calculate(
                        signal.symbol,
                        entry,
                        tp
                    ),

                        "risk": risk,
                        "reward": reward,

                        "rr": reward / risk if risk > 0 else 0,

                        "duration": duration

                    }

            # ==========================================
            # SELL TRADE
            # ==========================================

            elif direction == "SELL":

                # Stop Loss Hit
                if high >= sl:

                    profit = entry - sl
                    duration = i - start_index

                    return {

                        "result": "LOSS",

                        "entry_index": start_index,
                        "exit_index": i,

                        "entry_time": df.iloc[start_index]["time"],
                        "exit_time": df.iloc[i]["time"],

                        "entry_price": entry,
                        "exit_price": sl,

                        "stop_loss": sl,
                        "take_profit": tp,

                        "profit": profit,
                        "profit_pips": PipCalculator.calculate(
                        signal.symbol,
                        sl,
                        entry
                    ),

                        "risk": risk,
                        "reward": reward,

                        "rr": reward / risk if risk > 0 else 0,

                        "duration": duration

                    }

                # Take Profit Hit
                if low <= tp:

                    profit = entry - tp
                    duration = i - start_index

                    return {

                        "result": "WIN",

                        "entry_index": start_index,
                        "exit_index": i,

                        "entry_time": df.iloc[start_index]["time"],
                        "exit_time": df.iloc[i]["time"],

                        "entry_price": entry,
                        "exit_price": tp,

                        "stop_loss": sl,
                        "take_profit": tp,

                        "profit_pips": PipCalculator.calculate(
                        signal.symbol,
                        tp,
                         entry
                    ),

                        "risk": risk,
                        "reward": reward,

                        "rr": reward / risk if risk > 0 else 0,

                        "duration": duration

                    }

        # ==========================================
        # TRADE STILL OPEN
        # ==========================================

        duration = len(df) - start_index

        return {

            "result": "OPEN",

            "entry_index": start_index,
            "exit_index": len(df) - 1,

            "entry_time": df.iloc[start_index]["time"],
            "exit_time": None,

            "entry_price": entry,
            "exit_price": None,

            "stop_loss": sl,
            "take_profit": tp,

            "profit": 0,
            "profit_pips": 0,

            "risk": risk,
            "reward": reward,

            "rr": reward / risk if risk > 0 else 0,

            "duration": duration

        }