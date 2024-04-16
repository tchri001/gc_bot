import cv2
import numpy as np
import pyautogui
import autopy
import time
from threading import Thread

def fast_click(x, y):
    pyautogui.moveTo(x, y)
    pyautogui.click()

def slow_click(x, y):
    pyautogui.moveTo(x, y, 0.1)
    pyautogui.mouseDown()
    time.sleep(0.1)
    pyautogui.mouseUp()

def find_and_click(image: str, fast: bool = False):
    click_method = None
    if fast:
        click_method = fast_click
    else:
        click_method = slow_click
    image_to_find = 'images/'+image+'.png'
    x, y = pyautogui.locateCenterOnScreen(image_to_find, confidence=0.8)
    click_method(x, y)
    
if __name__ == '__main__':
    # t = Thread(target=find_and_click, args=('open_bluestacks',))
    # t.start()
    # t2 = Thread(target=find_and_click, args=('to_battle', True))
    # t2.start()
    find_and_click("open_bluestacks")
    time.sleep(1)
    find_and_click('to_battle', True)
    time.sleep(3)

    #Use threading for spamming abilities
    #Make this look only on the players half of the screen
    while True:
        find_and_click("activate", True)