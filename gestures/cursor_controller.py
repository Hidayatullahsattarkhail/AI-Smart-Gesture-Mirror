import pyautogui
import numpy as np

class CursorController:
    def __init__(self, screen_w, screen_h):
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.prev_x, self.prev_y = 0, 0
        self.smoothing = 5

    def move_cursor(self, x, y):
        # Interpolate / Smooth
        curr_x = self.prev_x + (x - self.prev_x) / self.smoothing
        curr_y = self.prev_y + (y - self.prev_y) / self.smoothing
        
        try:
            pyautogui.moveTo(curr_x, curr_y)
        except pyautogui.FailSafeException:
            pass
            
        self.prev_x, self.prev_y = curr_x, curr_y

    def click(self):
        try:
            pyautogui.click()
        except pyautogui.FailSafeException:
            pass

    def scroll(self, amount):
        try:
            pyautogui.scroll(amount)
        except pyautogui.FailSafeException:
            pass
