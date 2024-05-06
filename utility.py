import sys, os
import time
import pyautogui
import keyboard
#from main import activations, battles_played #This doesn't work, need to setup OOP to initialise gameplay object/class with tracking vars

class Utilities:
    def __init__(self, device, logger):
        self.device = device
        self.logger = logger

    def click_image(self, image, region=None, confidence=0.8):
        x,y = self.find_image(image, region, confidence)
        self.mouse_click(x,y)

    def find_image(self, image, region=None, confidence=0.8):
        image_path = 'images/'+self.device+'/'+image+'.png'

        if region:
            x,y = pyautogui.locateCenterOnScreen(image_path, region, confidence)
        else:
            x,y = pyautogui.locateCenterOnScreen(image_path, confidence)
        
        return x,y
    
    def mouse_click(self, x, y):
        pyautogui.moveTo(x, y)
        pyautogui.mouseDown()
        pyautogui.mouseUp()

#####----- REFACTORING ABOVE -----#####



    # Locate and click a passed in image
    def find_and_click(self, image, user_side = False, x_inc=1, y_inc=10, x_mult=1, y_mult=1, confidence=0.9):
        # Name of image on screen to find
        image_to_find = 'images/'+self.device+'/'+image+'.png'

        # Get coordinates of center point of image on screen
        x_raw, y_raw = self.locate_image(image_to_find, user_side, confidence)

        # Offset coordinates a little for hitbox
        x_offset = x_raw + (x_inc * x_mult)
        y_offset = y_raw + (y_inc * y_mult)
        self.logger.info(f'Clicking at: {x_offset} and {y_offset}')
        # Maybe check for activation colour at raw x,y (84, 188, 255), if not present return
        self.click(x_offset, y_offset)

    # Gets the x, y coordinates of whatever image is passed in
    def locate_image(self, image, side, conf):
        if side:
            # When side is True limit the region to left side of screen, this is where user sprites are
            x, y = pyautogui.locateCenterOnScreen(image, confidence=conf, region=(410, 250, 540, 480)) #Left, Top, Width, Height
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
            myScreenshot.save(f'images/'+self.device+'/screenshots/image{i}.png')
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