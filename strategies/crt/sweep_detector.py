"""
CRT Sweep Detector

Responsible for detecting liquidity sweeps
above or below the Higher Timeframe range.
"""

from models.sweep import Sweep

# ----------------------------------------
# Sweep Quality Filters
# ----------------------------------------

MIN_SWEEP_DISTANCE = 0.03      # Minimum sweep beyond HTF level
MIN_WICK_BODY_RATIO = 1.5      # Wick must be 1.5x candle body


class SweepDetector:

    @staticmethod
    def detect(df, htf_range):

        """
        Parameters
        ----------
        df : DataFrame
            Entry timeframe candles (typically M5)

        htf_range : HTFRange
            Higher timeframe range

        Returns
        -------
        Sweep
            if a valid sweep is detected

        None
            otherwise
        """

        if df is None or len(df) == 0:
            return None

        # Scan from oldest to newest
        # ----------------------------------------
        # Only check candles AFTER the HTF candle
        # ----------------------------------------

        filtered_df = df[df["time"] > htf_range.time]

        if len(filtered_df) == 0:
            return None

        # Scan from newest to oldest
        for i in range(len(filtered_df) - 1, -1, -1):

            candle = filtered_df.iloc[i]

            open_price = float(candle["open"])
            high = float(candle["high"])
            low = float(candle["low"])
            close = float(candle["close"])
            candle_time = candle["time"]

            # ----------------------------------------
            # Candle Measurements
            # ----------------------------------------

            body = abs(close - open_price)

            upper_wick = high - max(open_price, close)
            lower_wick = min(open_price, close) - low            

            # =====================================
            # BUY Sweep
            # =====================================

            if low < htf_range.low and close > htf_range.low:

                sweep_distance = htf_range.low - low

                # Reject tiny sweeps
                if sweep_distance < MIN_SWEEP_DISTANCE:
                    continue

                # Reject weak rejection candles
                if body > 0 and (lower_wick / body) < MIN_WICK_BODY_RATIO:
                    continue


                # print("\n========== SWEEP DETECTED ==========")
                # print(f"Time       : {candle_time}")
                # print(f"Direction  : BUY")
                # print(f"Open       : {open_price}")
                # print(f"High       : {high}")
                # print(f"Low        : {low}")
                # print(f"Close      : {close}")
                # print(f"HTF Low    : {htf_range.low}")
                # print("====================================")

                return Sweep(
                    valid=True,
                    direction="BUY",
                    sweep_price=low,
                    htf_level=htf_range.low,
                    candle_index=i,
                    candle_time=candle_time,
                    open=open_price,
                    high=high,
                    low=low,
                    close=close
                )

            # =====================================
            # SELL Sweep
            # =====================================

            if high > htf_range.high and close < htf_range.high:

                sweep_distance = high - htf_range.high

                # Reject tiny sweeps
                if sweep_distance < MIN_SWEEP_DISTANCE:
                    continue

                # Reject weak rejection candles
                if body > 0 and (upper_wick / body) < MIN_WICK_BODY_RATIO:
                    continue

                # print("\n========== SWEEP DETECTED ==========")
                # print(f"Time       : {candle_time}")
                # print(f"Direction  : SELL")
                # print(f"Open       : {open_price}")
                # print(f"High       : {high}")
                # print(f"Low        : {low}")
                # print(f"Close      : {close}")
                # print(f"HTF High   : {htf_range.high}")
                # print("====================================")

                return Sweep(
                    valid=True,
                    direction="SELL",
                    sweep_price=high,
                    htf_level=htf_range.high,
                    candle_index=i,
                    candle_time=candle_time,
                    open=open_price,
                    high=high,
                    low=low,
                    close=close
                )

        return None