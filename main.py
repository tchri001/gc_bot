import cv2
import numpy as np
import pyautogui
import autopy

if __name__ == '__main__':
    autopy.alert.alert("Waiting...")
    pyautogui.screenshot('images/screenshots/main_page.png')
    to_battle_loc = pyautogui.locateOnScreen('images/to_battle.png')
    print(to_battle_loc)