import cv2
import numpy as np
import pyautogui
import autopy
import time
from threading import Thread

# Quick click function, more reliable than pyautogui.click()
def click(x, y):
    pyautogui.moveTo(x, y)
    pyautogui.mouseDown()
    pyautogui.mouseUp()

def locate_function(image, side, conf):
    if side:
        # When side is True limit the region to left side of screen, this is where user sprites are
        x, y = pyautogui.locateCenterOnScreen(image, confidence=conf, region=(320, 0, 700, 1000))
    else:
        # By default use whole screen
        x, y = pyautogui.locateCenterOnScreen(image, confidence=conf)
    return x, y

def find_and_click(image, user_side = False, x_inc=1, y_inc=10, x_mult=1, y_mult=1, confidence=0.8):
    # Name of image on screen to find
    image_to_find = 'images/'+image+'.png'
    # Get coordinates of center point of image on screen
    x_raw, y_raw = locate_function(image_to_find, user_side, confidence)

    # Offset coordinates a little for hitbox
    x_offset = x_raw + x_inc * x_mult
    y_offset = y_raw + y_inc * y_mult
    click(x_offset, y_offset)

# Used to take screenshots for debugging
def screenies():
    i = 0
    t = time.time()
    while True:
        myScreenshot = pyautogui.screenshot()
        myScreenshot.save(f'images/screenshots/image{i}.png')
        i+=1
        time.sleep(.01) # Wait 10ms
        if time.time()-t>=3: # Take screenshots for 3 seconds total
            break

def run_game():
    # TODO: Use threading instead of sleep
    # TODO: Global variable to store in-game/in-menu status
    find_and_click("open_bluestacks")
    time.sleep(0.2)
    find_and_click('to_battle')
    time.sleep(0.2)
    pyautogui.press('esc')

    # TODO: Kill status inside loop, global variable?
    # TODO: When spamming activations if none are currently found but in-game status is true keep polling, currently dies when cant find any activations
    while True:
        find_and_click("activate", user_side=True)

if __name__ == '__main__':
    #pyautogui.displayMousePosition()
    run_game()