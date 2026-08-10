"""
====================================================
Scalping Pause Controller
====================================================
"""


class PauseController:

    def __init__(self):

        self._paused = False
        self._kill_requested = False

    # =====================================================
    # PAUSE
    # =====================================================

    def pause(self):

        self._paused = True

        print("[Scalping] Trading Paused")

    # =====================================================
    # RESUME
    # =====================================================

    def resume(self):

        self._paused = False

        print("[Scalping] Trading Resumed")

    # =====================================================
    # STATUS
    # =====================================================

    def is_paused(self):

        return self._paused

    # =====================================================
    # TOGGLE
    # =====================================================

    def toggle(self):

        self._paused = not self._paused

        print(
            f"[Scalping] Pause = {self._paused}"
        )

    # =====================================================
    # EMERGENCY KILL
    # =====================================================

    def request_kill(self):

        self._kill_requested = True

        print("[Scalping] Emergency Kill Requested")

    # =====================================================
    # CHECK KILL
    # =====================================================

    def kill_requested(self):

        return self._kill_requested

    # =====================================================
    # RESET KILL
    # =====================================================

    def reset_kill(self):

        self._kill_requested = False