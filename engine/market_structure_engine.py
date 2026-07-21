import pandas as pd


class MarketStructureEngine:

    def __init__(self, lookback=5):

     self.lookback = lookback

     self.bias = "SIDEWAYS"

    # --------------------------------------------------
    # Swing Detection
    # --------------------------------------------------

    def detect_swings(self, df):

        swings = []

        if len(df) < (self.lookback * 2 + 1):
            return swings

        for i in range(self.lookback, len(df) - self.lookback):

            high = df.iloc[i]["high"]
            low = df.iloc[i]["low"]

            swing_high = True
            swing_low = True

            # ------------------------------
            # Swing High
            # ------------------------------

            for j in range(1, self.lookback + 1):

                if high <= df.iloc[i - j]["high"]:
                    swing_high = False

                if high <= df.iloc[i + j]["high"]:
                    swing_high = False

            # ------------------------------
            # Swing Low
            # ------------------------------

            for j in range(1, self.lookback + 1):

                if low >= df.iloc[i - j]["low"]:
                    swing_low = False

                if low >= df.iloc[i + j]["low"]:
                    swing_low = False

            # ----------------------------------
            # Swing High
            # ----------------------------------

            if swing_high:

                new_swing = {

                    "type": "HIGH",

                    "index": i,

                    "time": df.iloc[i]["time"],

                    "price": high

                }

                if len(swings) == 0:

                    swings.append(new_swing)

                else:

                    last = swings[-1]

                    if last["type"] == "HIGH":

                        if new_swing["price"] > last["price"]:

                            swings[-1] = new_swing

                    else:

                        swings.append(new_swing)

            # ----------------------------------
            # Swing Low
            # ----------------------------------

            elif swing_low:

                new_swing = {

                    "type": "LOW",

                    "index": i,

                    "time": df.iloc[i]["time"],

                    "price": low

                }

                if len(swings) == 0:

                    swings.append(new_swing)

                else:

                    last = swings[-1]

                    if last["type"] == "LOW":

                        if new_swing["price"] < last["price"]:

                            swings[-1] = new_swing

                    else:

                        swings.append(new_swing)         

        return swings
    

    # --------------------------------------------------
    # Swing Classification
    # --------------------------------------------------

    def classify_swings(self, swings):
        """
        Classify swings as:

        HH = Higher High
        LH = Lower High
        HL = Higher Low
        LL = Lower Low
        """

        previous_high = None
        previous_low = None

        for swing in swings:

            if swing["type"] == "HIGH":

                if previous_high is None:
                    swing["structure"] = "HH"

                elif swing["price"] > previous_high:
                    swing["structure"] = "HH"

                else:
                    swing["structure"] = "LH"

                previous_high = swing["price"]

            else:

                if previous_low is None:
                    swing["structure"] = "LL"

                elif swing["price"] > previous_low:
                    swing["structure"] = "HL"

                else:
                    swing["structure"] = "LL"

                previous_low = swing["price"]

        return swings


    # --------------------------------------------------
    # Last Swing High
    # --------------------------------------------------

    def last_high(self, swings):

        for swing in reversed(swings):

            if swing["type"] == "HIGH":
                return swing

        return None

    # --------------------------------------------------
    # Last Swing Low
    # --------------------------------------------------

    def last_low(self, swings):

        for swing in reversed(swings):

            if swing["type"] == "LOW":
                return swing

        return None

    # --------------------------------------------------
    # Trend
    # --------------------------------------------------

    def detect_trend(self, swings, bos, choch):
        """
        Trend V2

        Priority:
        1. CHOCH determines trend change.
        2. Otherwise use swing structure as fallback.
        """

        # ----------------------------------
        # CHOCH changes the trend immediately
        # ----------------------------------

        if choch["valid"]:

            if choch["direction"] == "BUY":
                return "BULLISH"

            if choch["direction"] == "SELL":
                return "BEARISH"

        # ----------------------------------
        # Fallback to Swing Structure
        # ----------------------------------

        highs = [s for s in swings if s["type"] == "HIGH"]
        lows = [s for s in swings if s["type"] == "LOW"]

        if len(highs) < 2 or len(lows) < 2:
            return "SIDEWAYS"

        last_high = highs[-1]["price"]
        prev_high = highs[-2]["price"]

        last_low = lows[-1]["price"]
        prev_low = lows[-2]["price"]

        if last_high > prev_high and last_low > prev_low:
            return "BULLISH"

        if last_high < prev_high and last_low < prev_low:
            return "BEARISH"

        return "SIDEWAYS"
    # --------------------------------------------------
    # Detect
    # --------------------------------------------------

    def detect(self, df):

        swings = self.detect_swings(df)

        swings = self.classify_swings(swings)

        protected = self.get_protected_swings(swings)

        bos = self.detect_bos(df, swings)

        trend = self.detect_trend(
            swings,
            bos,
            {
                "valid": False,
                "direction": None
            }
        )

        choch = self.detect_choch(bos, trend)
        mss = self.detect_mss(bos, trend)

        trend = self.detect_trend(
            swings,
            bos,
            choch
        )

        # --------------------------------------------------
        # Structure State (Temporary)
        # --------------------------------------------------

        internal_structure = None
        swing_structure = None
        strong_high = None
        strong_low = None
        

        return {

            "trend": trend,

            "swings": swings,

            "last_high": self.last_high(swings),

            "last_low": self.last_low(swings),

            "protected_high": protected["protected_high"],

            "protected_low": protected["protected_low"],

            "strong_high": strong_high,

            "strong_low": strong_low,

            "internal_structure": internal_structure,

            "swing_structure": swing_structure,

            
            "mss": mss,
            "bos": bos,

            "choch": choch
            

        }
    # --------------------------------------------------
    # Protected Swings
    # --------------------------------------------------

    def get_protected_swings(self, swings):

        protected_high = None
        protected_low = None

        for swing in reversed(swings):

            if protected_high is None and swing["type"] == "HIGH":
                protected_high = swing

            if protected_low is None and swing["type"] == "LOW":
                protected_low = swing

            if protected_high and protected_low:
                break

        return {

            "protected_high": protected_high,

            "protected_low": protected_low

        }    
    
    # --------------------------------------------------
    # BOS Detection
    # --------------------------------------------------

    def detect_bos(self, df, swings):
        """
        Professional BOS V2

        Uses:
        - Swing High / Swing Low
        - Candle Close Confirmation
        - Previous Close Confirmation

        Returns:
        {
            "valid": bool,
            "direction": "BUY" / "SELL" / None,
            "break_price": float | None,
            "broken_swing": dict | None
        }
        """

        if len(df) < 2:
            return {
                "valid": False,
                "direction": None,
                "break_price": None,
                "broken_swing": None
            }

        highs = [s for s in swings if s["type"] == "HIGH"]
        lows = [s for s in swings if s["type"] == "LOW"]

        if not highs or not lows:
            return {
                "valid": False,
                "direction": None,
                "break_price": None,
                "broken_swing": None
            }

        last_high = highs[-1]
        last_low = lows[-1]

        current_close = df.iloc[-1]["close"]
        previous_close = df.iloc[-2]["close"]

        # ----------------------------------
        # Bullish BOS
        # ----------------------------------

        if (
            current_close > last_high["price"]
            and previous_close <= last_high["price"]
        ):

            structure_type = "BOS"

            if self.bias == "BEARISH":
                structure_type = "CHOCH"

            self.bias = "BULLISH"

            return {
                "valid": True,
                "type": structure_type,
                "direction": "BUY",
                "break_price": last_high["price"],
                "broken_swing": last_high
            }

        # ----------------------------------
        # Bearish BOS
        # ----------------------------------

        if (
            current_close < last_low["price"]
            and previous_close >= last_low["price"]
        ):

            structure_type = "BOS"

            if self.bias == "BULLISH":
                structure_type = "CHOCH"

            self.bias = "BEARISH"

            return {
                "valid": True,
                "type": structure_type,
                "direction": "SELL",
                "break_price": last_low["price"],
                "broken_swing": last_low
            }

        return {
            "valid": False,
            "type": None,
            "direction": None,
            "break_price": None,
            "broken_swing": None
        }
    # --------------------------------------------------
    # CHOCH Detection
    # --------------------------------------------------

     # --------------------------------------------------
    # CHOCH Detection
    # --------------------------------------------------

    def detect_choch(self, bos, trend):
        """
        CHOCH V1

        CHOCH occurs when:
        - Current BOS direction is opposite to current trend.
        """

        if not bos["valid"]:
            return {
                "valid": False,
                "direction": None
            }

        # ----------------------------------
        # Bullish CHOCH
        # ----------------------------------

        if trend == "BEARISH" and bos["direction"] == "BUY":
            return {
                "valid": True,
                "direction": "BUY"
            }

        # ----------------------------------
        # Bearish CHOCH
        # ----------------------------------

        if trend == "BULLISH" and bos["direction"] == "SELL":
            return {
                "valid": True,
                "direction": "SELL"
            }

        return {
            "valid": False,
            "direction": None
        }
    
    # --------------------------------------------------
    # MSS Detection
    # --------------------------------------------------

    def detect_mss(self, bos, trend):
        """
        MSS V1

        Market Structure Shift

        Requirements:
        - Valid BOS
        - BOS agrees with current trend
        """

        if not bos["valid"]:
            return {
                "valid": False,
                "direction": None
            }

        # Bullish MSS

        if trend == "BULLISH" and bos["direction"] == "BUY":
            return {
                "valid": True,
                "direction": "BUY"
            }

        # Bearish MSS

        if trend == "BEARISH" and bos["direction"] == "SELL":
            return {
                "valid": True,
                "direction": "SELL"
            }

        return {
            "valid": False,
            "direction": None
        }    