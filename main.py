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
        utils.find_and_click('to_battle')
        #battles_played += 1 #For some reason this stops the script
        time.sleep(0.2)
        pyautogui.press('esc')

    # Spam abilities whilst in game
    def play_battle(self):
        global game_status

        while game_status == 1:
            try:
                utils.find_and_click("activate", user_side=True)
                logger.info('ACTIVATE!!!')
                #activations += 1 #For some reason this stops the script
            except pyautogui.ImageNotFoundException as e:
                time.sleep(1)
                logger.info('Waiting for refresh')

    def game_status_actions(self):
        global game_status
        while True:
            try:
                pyautogui.locateOnScreen(f'images/'+device+'/settings.png')
                game_status = 0
                logger.info('Settings found, status = home screen')
                self.enter_game()
            except pyautogui.ImageNotFoundException: 
                game_status = 1
                logger.info('Settings not found, status = in game')
                self.play_battle() #TODO: I don't think this should be here, maybe multithread it?
                time.sleep(1)

if __name__ == '__main__':
    # Icons don't work across device so change this as needed
    #device = 'laptop'
    device = 'pc'

    # Configure and create logger
    logging.basicConfig(filename="gc_bot.log", format='%(asctime)s %(message)s', filemode='w', level=logging.INFO)
    logger = logging.getLogger()

    utils = Utilities(logger)
    bot = GameBot(device, utils, logger)

    # Start up exit on input thread
    exit_program = threading.Thread(target=utils.user_exit, args=(logger,))
    exit_program.start()
    
    # Setup threads, game status keeps the var updated and gameplay does the actual interaction
    play_game = threading.Thread(target=bot.game_status_actions, args=())

    # Open up the game then start 
    # TODO: Check this out for window handling instead of relying on game icon: https://stackoverflow.com/questions/43785927/python-pyautogui-window-handle
    logger.info('Opening Emulator taskbar icon')
    utils.find_and_click("open_bluestacks")
    time.sleep(0.5)

    # Start both threads to kick off playing
    logger.info('Starting program...')
    play_game.start() # I have this entering and playing games atm