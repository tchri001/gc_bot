import os
import pyautogui
import keyboard

class Utils:
    def __init__(self, device, logger):
        self.device = device
        self.logger = logger

    #Find an image with optional screen region constraint
    def find_image(self, image, confidence=0.8, region=None):
        image_path = 'images/'+self.device+'/'+image+'.png'

        if region:
            x,y = pyautogui.locateCenterOnScreen(image_path, confidence=confidence, region=region)
        else:
            x,y = pyautogui.locateCenterOnScreen(image_path, confidence=confidence)
        
        return x,y
    
    #Click on passed in coordinates (more reliable than pyautogui.click())
    def mouse_click(self, x, y):
        pyautogui.moveTo(x, y)
        pyautogui.mouseDown()
        pyautogui.mouseUp()

    #Chain find and click together
    def click_image(self, image, region=None, confidence=0.8):
        x,y = self.find_image(image, region, confidence)
        self.mouse_click(x,y)

    #Polling function to exit program on 'q' key press
    def exit_program(self):
        while True:
            if keyboard.is_pressed('q'):
                self.logger.info('EXITING PROGRAM')
                os.exit(1)