"""
CRT Validation

Validates whether a detected sweep
is a valid CRT setup.
"""


class Validation:

    @staticmethod
    def validate(sweep, htf_range):

        """
        Parameters
        ----------
        sweep : Sweep

        htf_range : HTFRange

        Returns
        -------
        bool
        """

        # No sweep detected
        if sweep is None:
            return False

        # -----------------------------
        # BUY Validation
        # -----------------------------
        if sweep.direction == "BUY":

            return sweep.close > htf_range.low

        # -----------------------------
        # SELL Validation
        # -----------------------------
        if sweep.direction == "SELL":

            return sweep.close < htf_range.high

        return False