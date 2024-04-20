import sys, os
import time
import pyautogui
import keyboard
from main import device
#from main import activations, battles_played #This doesn't work, need to setup OOP to initialise gameplay object/class with tracking vars

class Utilities:
    def __init__(self, logger):
        self.logger = logger

    # Locate and click a passed in image
    def find_and_click(self, image, user_side = False, x_inc=1, y_inc=10, x_mult=1, y_mult=1, confidence=0.8):
        # Name of image on screen to find
        image_to_find = 'images/'+device+'/'+image+'.png'

        # Get coordinates of center point of image on screen
        x_raw, y_raw = self.locate_function(image_to_find, user_side, confidence)

        # Offset coordinates a little for hitbox
        x_offset = x_raw + x_inc * x_mult
        y_offset = y_raw + y_inc * y_mult
        self.click(x_offset, y_offset)

    # Gets the x, y coordinates of whatever image is passed in
    def locate_function(self, image, side, conf):
        if side:
            # When side is True limit the region to left side of screen, this is where user sprites are
            x, y = pyautogui.locateCenterOnScreen(image, confidence=conf, region=(320, 0, 700, 1000))
        else:
            # By default use whole screen
            x, y = pyautogui.locateCenterOnScreen(image, confidence=conf)
        return x, y

    # Quick click function, more reliable than pyautogui.click()
    def click(self, x, y):
        pyautogui.moveTo(x, y)
        pyautogui.mouseDown()
        pyautogui.mouseUp()

    # Used to take screenshots for debugging
    def screenies(self):
        i = 0
        t = time.time()
        while True:
            myScreenshot = pyautogui.screenshot()
            myScreenshot.save(f'images/'+device+'/screenshots/image{i}.png')
            i+=1
            time.sleep(.01) # Wait 10ms
            if time.time()-t>=3: # Take screenshots for 3 seconds total
                break

    # Monitor function to kill program is 'q' pressed
    def user_exit(self, logger):
        while True:
            if keyboard.is_pressed('q'):
                logger.info('EXITING PROGRAM')
                # TODO: Bit of a violent ending but haven't found another way to end the main thread yet, maybe thread.interrupt_main() or something
                #logger.info(f'Games stats\nActivations: {activations}\nBattles played: {battles_played}')
                os._exit(1)        