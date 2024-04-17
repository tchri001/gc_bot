import cv2
import numpy as np
import pyautogui
import autopy
import time
from threading import Thread

def click(x, y):
    pyautogui.moveTo(x, y)
    pyautogui.click()

# def slow_click(x, y):
#     pyautogui.moveTo(x, y, 0.1)
#     pyautogui.mouseDown()
#     time.sleep(0.1)
#     pyautogui.mouseUp()

def find_and_click(image: str, user_side: bool = False):
    image_to_find = 'images/'+image+'.png'

    if user_side:
        x, y = pyautogui.locateCenterOnScreen(image_to_find, confidence=0.8, region=(0, 0, 1000, 1000))
    else:
        x, y = pyautogui.locateCenterOnScreen(image_to_find, confidence=0.8)

    y_offset = y + 10
    click(x, y_offset)
    
if __name__ == '__main__':
    # t = Thread(target=find_and_click, args=('open_bluestacks',))
    # t.start()
    # t2 = Thread(target=find_and_click, args=('to_battle', True))
    # # t2.start()
    find_and_click("open_bluestacks")
    time.sleep(0.5)
    find_and_click('to_battle')
    time.sleep(3) #find and click the X button on the start timer

    #Use threading for spamming abilities
    #Kill loop on user input
    try:
        while True:
        #global variable to save in-game or in-menu status, threading?
        #if no activate currently found but in-game is true keep polling
            find_and_click("activate", user_side=True)
    except KeyboardInterrupt:
        pass
    #pyautogui.displayMousePosition() #just for finding coordinates during a game
