import cv2
import numpy as np
import pyautogui
import autopy

if __name__ == '__main__':
    autopy.alert.alert("Waiting...")
    pyautogui.screenshot('images/screenshots/main_page.png')
