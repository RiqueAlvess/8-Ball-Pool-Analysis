'''Input Execution Module'''

import math
import time

try:
    import pyautogui
    _PYAUTOGUI_AVAILABLE = True
except Exception:
    _PYAUTOGUI_AVAILABLE = False


class InputExecutor:
    '''
    Translates a calculated pool shot into physical mouse input via pyautogui.

    The shot is executed as a click-drag on the white ball:
      1. Move cursor to the white ball's screen position.
      2. Press and hold the mouse button.
      3. Drag backward (opposite shot direction) to set power.
      4. Release to fire.

    Captured-frame coordinates are converted to absolute screen coordinates
    by adding the capture region's top-left offset.
    '''

    MAX_DRAG_PX = 150
    FORCE_SCALE = 0.35
    PRE_SHOT_PAUSE = 0.3
    DRAG_DURATION = 0.4
    HOLD_DURATION = 0.4

    def __init__(self):
        if not _PYAUTOGUI_AVAILABLE:
            print('[InputExecutor] pyautogui is not available — shot execution disabled.')

    @property
    def available(self):
        return _PYAUTOGUI_AVAILABLE

    def execute_shot(self, white_frame, target_frame, capture_offset):
        '''
        Fire a shot given frame-relative coordinates.

        white_frame:     (x, y) white ball position inside the captured frame
        target_frame:    (x, y) target hit position inside the captured frame
        capture_offset:  (left, top) pixel offset of the capture region on screen
        '''
        if not _PYAUTOGUI_AVAILABLE:
            return

        white_abs = (
            white_frame[0] + capture_offset[0],
            white_frame[1] + capture_offset[1],
        )
        target_abs = (
            target_frame[0] + capture_offset[0],
            target_frame[1] + capture_offset[1],
        )

        dx = target_abs[0] - white_abs[0]
        dy = target_abs[1] - white_abs[1]
        dist = math.sqrt(dx ** 2 + dy ** 2) or 1e-9

        nx, ny = dx / dist, dy / dist

        drag_pixels = min(dist * self.FORCE_SCALE, self.MAX_DRAG_PX)
        drag_x = int(white_abs[0] - nx * drag_pixels)
        drag_y = int(white_abs[1] - ny * drag_pixels)

        pyautogui.moveTo(white_abs[0], white_abs[1], duration=self.PRE_SHOT_PAUSE)
        pyautogui.mouseDown()
        pyautogui.moveTo(drag_x, drag_y, duration=self.DRAG_DURATION)
        time.sleep(self.HOLD_DURATION)
        pyautogui.mouseUp()
