import numpy as np
import pyautogui
import time
import threading
import sys, os
import logging
from utility import Utilities

class GameBot:
    def __init__(self, device, utils: Utilities, logger):
        self.device = device
        self.utils = utils
        self.logger = logger
        # Stat tracking variables
        self.game_status = 0
        self.activations = 0
        self.battles_played = 0

    # Enter into a battle
    def enter_game(self):
        logger.info('Entering battle...')
        utils.click_image('to_battle', region=(1670, 780, 200, 200))
        #battles_played += 1 #For some reason this stops the script
        time.sleep(0.2)
        pyautogui.press('esc')

    # Spam abilities whilst in game
    def play_battle(self):
        global game_status

        while True:
            if game_status == 0:
                logger.info('Entering battle')
                self.enter_game()
            else:
                try:
                    utils.click_image("activate", region=(410, 250, 540, 480))
                except pyautogui.ImageNotFoundException as e:
                    time.sleep(0.5)
                    logger.info('Waiting for refresh')
    
    def status(self):
        global game_status
        game_status = 0

        while True:
            try:
                utils.find_image('settings', region=(320, 840, 130, 130))
                logger.info('Settings found, status = home screen')
                game_status = 0
                time.sleep(0.5)
            except pyautogui.ImageNotFoundException:
                logger.info('Settings not found, status = in game')
                game_status = 1
                time.sleep(0.5)


if __name__ == '__main__':
    #device = 'laptop'
    device = 'pc'

    # Configure and create logger
    logging.basicConfig(filename="gc_bot.log", format='%(asctime)s %(message)s', filemode='w', level=logging.INFO)
    logger = logging.getLogger()

    utils = Utilities(device, logger)
    bot = GameBot(device, utils, logger)

    # Start up exit on input thread
    exit_program = threading.Thread(target=utils.user_exit, args=(logger,))
    exit_program.start()

    #Status tracker
    status_poller = threading.Thread(target=bot.status, args=())
    status_poller.start()

    # Setup threads, game status keeps the var updated and gameplay does the actual interaction
    play_game = threading.Thread(target=bot.game_status_actions, args=())

    #####----- GAMEPLAY STARTS HERE -----#####
    # TODO: Check this out for window handling instead of relying on game icon: https://stackoverflow.com/questions/43785927/python-pyautogui-window-handle
    x, y = utils.find_image('open_bluestacks')
    pyautogui.click(x, y)
    time.sleep(0.5)

    # Start both threads to kick off playing
    logger.info('Starting program...')
    play_game.start() # I have this entering and playing games atm