import pandas as pd


class Structure:

    @staticmethod
    def detect_swings(df, lookback=5):

        swings = []

        if len(df) < (lookback * 2 + 1):
            return swings

        for i in range(lookback, len(df) - lookback):

            high = df.iloc[i]["high"]
            low = df.iloc[i]["low"]

            is_swing_high = True
            is_swing_low = True

            # -----------------------------
            # Check Swing High
            # -----------------------------

            for j in range(1, lookback + 1):

                if high <= df.iloc[i - j]["high"]:
                    is_swing_high = False

                if high <= df.iloc[i + j]["high"]:
                    is_swing_high = False

            # -----------------------------
            # Check Swing Low
            # -----------------------------

            for j in range(1, lookback + 1):

                if low >= df.iloc[i - j]["low"]:
                    is_swing_low = False

                if low >= df.iloc[i + j]["low"]:
                    is_swing_low = False

            if is_swing_high:

                swings.append({

                    "type": "HIGH",

                    "index": i,

                    "time": df.iloc[i]["time"],

                    "price": high

                })

            elif is_swing_low:

                swings.append({

                    "type": "LOW",

                    "index": i,

                    "time": df.iloc[i]["time"],

                    "price": low

                })

        return swings

    @staticmethod
    def classify_swings(swings):

        if len(swings) < 2:
            return []

        structure = []

        last_high = None
        last_low = None

        for swing in swings:

            # --------------------------------
            # Swing High
            # --------------------------------

            if swing["type"] == "HIGH":

                if last_high is None:

                    label = "SH"

                elif swing["price"] > last_high:

                    label = "HH"

                else:

                    label = "LH"

                last_high = swing["price"]

            # --------------------------------
            # Swing Low
            # --------------------------------

            else:

                if last_low is None:

                    label = "SL"

                elif swing["price"] > last_low:

                    label = "HL"

                else:

                    label = "LL"

                last_low = swing["price"]

            structure.append({

                "label": label,

                "type": swing["type"],

                "time": swing["time"],

                "price": swing["price"]

            })

        return structure 

    
    @staticmethod
    def get_last_swing_high(swings):

        for swing in reversed(swings):

            if swing["type"] == "HIGH":

                return swing

        return None


    @staticmethod
    def get_last_swing_low(swings):

        for swing in reversed(swings):

            if swing["type"] == "LOW":

                return swing

        return None

    @staticmethod
    def detect_bos(df, last_high, last_low):

        if len(df) == 0:
            return None

        candle = df.iloc[-1]

        # -----------------------------
        # Bullish BOS
        # -----------------------------

        if last_high:

            if candle["close"] > last_high["price"]:

                return {

                    "bos": True,

                    "direction": "BUY",

                    "level": last_high["price"],

                    "time": candle["time"]

                }

        # -----------------------------
        # Bearish BOS
        # -----------------------------

        if last_low:

            if candle["close"] < last_low["price"]:

                return {

                    "bos": True,

                    "direction": "SELL",

                    "level": last_low["price"],

                    "time": candle["time"]

                }

        return {

            "bos": False,

            "direction": None,

            "level": None,

            "time": None

        }        