'''Input Execution Module'''

import math
import time

try:
    import pyautogui
    pyautogui.FAILSAFE = True   # move mouse to top-left corner to abort
    pyautogui.PAUSE = 0.0       # we control timing ourselves
    _PYAUTOGUI_AVAILABLE = True
except Exception:
    _PYAUTOGUI_AVAILABLE = False


class InputExecutor:
    '''
    Translates a calculated pool shot into mouse input for the desktop game.

    Control scheme (8 Ball Pool desktop):
      1. Hover the mouse to the AIM POSITION (behind the white ball, on the
         opposite side of the intended shot direction). The game registers the
         cue angle from the mouse position relative to the cue ball.
      2. Press and hold left mouse button at the aim position.
      3. Drag further back (away from white ball) to set shot power.
      4. Release to fire.

    Frame coordinates are converted to absolute screen coordinates by adding
    the capture region's top-left offset.
    '''

    AIM_DISTANCE = 80    # px from white ball centre to hover for aiming
    MAX_DRAG_PX  = 120   # maximum additional drag for full power
    FORCE_SCALE  = 0.30  # game_distance_px → drag_px multiplier

    AIM_DURATION   = 0.20  # seconds to move mouse to aim position
    AIM_SETTLE     = 0.15  # pause after hover so game can register angle
    DRAG_DURATION  = 0.35  # seconds for the power drag
    RELEASE_PAUSE  = 0.10  # pause before releasing

    def __init__(self):
        if not _PYAUTOGUI_AVAILABLE:
            print('[InputExecutor] pyautogui not available — shot execution disabled.')

    @property
    def available(self):
        return _PYAUTOGUI_AVAILABLE

    def execute_shot(self, white_frame, target_frame, capture_offset):
        '''
        Fire a shot.

        white_frame:    (x, y) white ball centre in captured-frame coordinates
        target_frame:   (x, y) target hit position in captured-frame coordinates
        capture_offset: (left, top) pixel offset of the capture region on screen
        '''
        if not _PYAUTOGUI_AVAILABLE:
            return

        # Map frame → screen coordinates
        white_abs  = (white_frame[0]  + capture_offset[0], white_frame[1]  + capture_offset[1])
        target_abs = (target_frame[0] + capture_offset[0], target_frame[1] + capture_offset[1])

        # Unit vector: white ball → target (shot direction)
        dx = target_abs[0] - white_abs[0]
        dy = target_abs[1] - white_abs[1]
        dist = math.sqrt(dx ** 2 + dy ** 2) or 1e-9
        nx, ny = dx / dist, dy / dist

        # Aim position: behind white ball (opposite to shot direction)
        aim_x = int(white_abs[0] - nx * self.AIM_DISTANCE)
        aim_y = int(white_abs[1] - ny * self.AIM_DISTANCE)

        # Drag-back position: further behind for power (proportional to shot distance)
        drag_extra = min(dist * self.FORCE_SCALE, self.MAX_DRAG_PX)
        drag_x = int(white_abs[0] - nx * (self.AIM_DISTANCE + drag_extra))
        drag_y = int(white_abs[1] - ny * (self.AIM_DISTANCE + drag_extra))

        # Step 1 — hover to aim (no click, game registers angle from cursor position)
        pyautogui.moveTo(aim_x, aim_y, duration=self.AIM_DURATION)
        time.sleep(self.AIM_SETTLE)

        # Step 2 — press, drag back for power, release
        pyautogui.mouseDown(button='left')
        pyautogui.moveTo(drag_x, drag_y, duration=self.DRAG_DURATION)
        time.sleep(self.RELEASE_PAUSE)
        pyautogui.mouseUp(button='left')
