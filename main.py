import cv2
import numpy as np
import pyautogui
import autopy
import time
from threading import Thread

#Quick click function, more reliable than pyautogui.click()
def click(x, y):
    pyautogui.moveTo(x, y)
    pyautogui.mouseDown()
    pyautogui.mouseUp()

def locate_function(image, side, conf):
    if side:
        #When side is True limit the region to left side of screen, this is where user sprites are
        x, y = pyautogui.locateCenterOnScreen(image, confidence=conf, region=(320, 0, 700, 1000))
    else:
        #By default use whole screen
        x, y = pyautogui.locateCenterOnScreen(image, confidence=conf)
    return x, y

def find_and_click(image, user_side = False, x_inc=1, y_inc=10, x_mult=1, y_mult=1, confidence=0.8):
    #Name of image on screen to find
    image_to_find = 'images/'+image+'.png'
    #Get coordinates of center point of image on screen
    x_raw, y_raw = locate_function(image_to_find, user_side, confidence)

    #Offset coordinates a little for hitbox
    x_offset = x_raw + x_inc * x_mult
    y_offset = y_raw + y_inc * y_mult
    click(x_offset, y_offset)

#Used to take screenshots 10ms apart for 3 seconds
def screenies():
    i = 0
    t = time.time()
    while True:
        myScreenshot = pyautogui.screenshot()
        myScreenshot.save(f'images/screenshots/image{i}.png')
        i+=1
        time.sleep(.01)
        if time.time()-t>=3: # Instead of 10s write the time of your video in second.
            break

def run_game():
    # t = Thread(target=find_and_click, args=('open_bluestacks',))
    # t.start()
    # t2 = Thread(target=find_and_click, args=('to_battle', True))
    # # t2.start()

    find_and_click("open_bluestacks")
    time.sleep(0.5)
    find_and_click('to_battle')
    time.sleep(0.5)
    find_and_click('wave_skip_exit', x_inc=45, x_mult=-1, confidence=0.4)
    #screenies()

    #Use threading for spamming abilities
    # #Kill loop on user input
    # while True:
    #     #global variable to save in-game or in-menu status, threading?
    #     #if no activate currently found but in-game is true keep polling
    #     find_and_click("activate", user_side=True)


if __name__ == '__main__':
    #pyautogui.displayMousePosition()
    run_game()