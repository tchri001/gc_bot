import os
import pyautogui
import time
import random
from gc_utils import Utils

game_status = 0

class Bot:
    def __init__(self, device, utils: Utils, logger):
        self.device = device
        self.utils = utils
        self.logger = logger

    #Close any menus to return to home screen
    def close_menus(self):
        home_screen = 0

        while home_screen == 0:
            try:
                self.utils.find_image('to_battle', region=(1670, 780, 200, 200))
                self.logger.debug('Home screen is open')
                home_screen = 1
            except pyautogui.ImageNotFoundException:
                self.logger.debug('Sub-menu open, closing it')
                pyautogui.press('esc')
                continue

    #Enter battle
    def to_battle(self):
        global game_status
        while game_status == 0:
            try:
                self.utils.click_image('to_battle', region=(1670, 780, 200, 200))
                self.logger.debug('Entering new battle')
                time.sleep(random.uniform(0.2, 0.5))
                pyautogui.press('esc')
                game_status = 1
                self.utils.games_played += 1
            except pyautogui.ImageNotFoundException:
                self.logger.debug("Couldn't enter new battle")
                self.close_menus()
                continue

    #Spam abilities at slightly randomised intervals
    def activate_abilities(self):
        global game_status
        
        while game_status == 1:
            try:
                self.utils.click_image('activate', region=(400, 220, 600, 600))
                time.sleep(random.uniform(0.2,0.3))
            except pyautogui.ImageNotFoundException:
                self.logger.debug('Waiting for refresh')
                break

    #Constantly poll for game status
    def game_status(self):
        global game_status

        while True:
            try:
                self.utils.find_image('settings', region=(320, 840, 130, 130))
                prev_status = game_status
                game_status = 0
                if prev_status != game_status:
                    self.logger.debug(f'Game status changed to home screen')
                time.sleep(0.2)
            except pyautogui.ImageNotFoundException:
                prev_status = game_status
                game_status = 1
                if prev_status != game_status:
                    self.logger.debug(f'Game status changed to in-game')
                time.sleep(0.2)
        
    #Core loop. Enter game or spam abilities
    def gameplay_loop(self):
        global game_status

        while True:
            if game_status == 0:
                self.to_battle()
            else:
                self.logger.debug('Activating abilities')
                self.activate_abilities()