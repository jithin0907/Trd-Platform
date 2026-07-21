from strategies.crt.config import SL_BUFFER_PIPS
from utils.pip_calculator import PipCalculator
from utils.pip_calculator import PipCalculator


"""
CRT Trade Levels

Responsible for calculating

- Entry
- Stop Loss
- Take Profit
- Risk Reward
"""

from strategies.crt.config import (
    SL_BUFFER_PIPS,
    TP_MODE,
    RISK_REWARD
)


class TradeLevels:

    @staticmethod
    def calculate(symbol, sweep, htf_range):


        buffer = PipCalculator.pips_to_price(
        symbol,
        SL_BUFFER_PIPS
)

        """
        Parameters
        ----------
        sweep : Sweep

        htf_range : HTFRange

        Returns
        -------
        dict
        """

        if sweep is None:
            return None

        # ---------------------------------
        # BUY
        # ---------------------------------

        if sweep.direction == "BUY":

            entry = sweep.close

            sl = sweep.low - buffer

            if TP_MODE == "OPPOSITE_RANGE":

                tp = htf_range.high

            elif TP_MODE == "MID_RANGE":

                tp = htf_range.mid

            elif TP_MODE == "RR":

                risk = entry - sl
                tp = entry + (risk * RISK_REWARD)

            else:

                tp = htf_range.high

        # ---------------------------------
        # SELL
        # ---------------------------------

        else:

            entry = sweep.close

            sl = sweep.high + buffer

            if TP_MODE == "OPPOSITE_RANGE":

                tp = htf_range.low

            elif TP_MODE == "MID_RANGE":

                tp = htf_range.mid

            elif TP_MODE == "RR":

                risk = sl - entry
                tp = entry - (risk * RISK_REWARD)

            else:

                tp = htf_range.low

        # ---------------------------------
        # Risk Reward
        # ---------------------------------

        risk = abs(entry - sl)
        reward = abs(tp - entry)

        rr = 0

        if risk != 0:
            rr = reward / risk

        return {

            "entry": round(entry, 5),
            "stop_loss": round(sl, 5),
            "take_profit": round(tp, 5),
            "risk_reward": round(rr, 2)

        }