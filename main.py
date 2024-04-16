import cv2
import numpy as np
import pyautogui
import autopy
import time

def fast_click(x, y):
    pyautogui.moveTo(x, y, 0)
    pyautogui.click()

def slow_click(x, y):
    pyautogui.moveTo(x, y, 0.1)
    pyautogui.mouseDown()
    time.sleep(0.1)
    pyautogui.mouseUp()

def find_and_click(image, fast: bool = False):
    click_method = None
    if fast:
        click_method = fast_click
    else:
        slow_click
    print('images/'+image+'.png')
    x, y = pyautogui.locateCenterOnScreen('images/'+image+'.png', confidence=0.8)
    click_method
    
if __name__ == '__main__':
    #autopy.alert.alert("Waiting...")
    bs_x, bs_y = pyautogui.locateCenterOnScreen('images/open_bluestacks.png', confidence=0.8)
    pyautogui.moveTo(bs_x, bs_y, 0.4)
    pyautogui.mouseDown()
    time.sleep(0.2)
    pyautogui.mouseUp()    

    bt_x, bt_y = pyautogui.locateCenterOnScreen('images/to_battle.png', confidence=0.8)
    pyautogui.moveTo(bt_x, bt_y, 1)
    pyautogui.mouseDown()
    time.sleep(0.2)
    pyautogui.mouseUp()