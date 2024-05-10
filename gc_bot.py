import pyautogui
import time
import random
from gc_utils import Utils

class Bot:
    def __init__(self, device, utils: Utils, logger):
        self.device = device
        self.utils = utils
        self.logger = logger
        self.game_status = 0

    #Enter battle
    def to_battle(self):
        global game_status
        self.logger.debug('Entering new battle')
        self.utils.click_image('to_battle', region=(1670, 780, 200, 200))
        self.game_status = 1
        time.sleep(random.uniform(0.2, 0.5))
        pyautogui.press('esc')

    #Spam abilities at slightly randomised intervals
    def activate_abilities(self):
        while True:
            try:
                self.utils.click_image('activate', region=(400, 220, 600, 600))
                self.logger.debug('Activating ability')
            except pyautogui.ImageNotFoundException:
                self.logger.debug('Waiting for refresh')
                time.sleep(random.uniform(0.2, 0.4))

    #Constantly poll for game status
    def game_status(self):
        global game_status

        while True:
            try:
                self.utils.find_image('settings', region=(320, 840, 130, 130))
                self.logger.debug('Status = Home Screen')
                self.game_status = 0
                time.sleep(0.2)
            except pyautogui.ImageNotFoundException:
                self.logger.debug('Status = In Game')
                self.game_status = 1
                time.sleep(0.2)
        
    #Core loop. Enter game or spam abilities
    def gameplay_loop(self):
        global game_status

        while True:
            if self.game_status == 0:
                self.to_battle()
            else:
                self.activate_abilities()