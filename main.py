import numpy as np
import pyautogui
import time
import threading
import sys
import logging
from utility import *

# Icons don't work across device so change this as needed
device = 'laptop'
#device = 'pc'

def run_game():
    global game_status
    # TODO: Use threading instead of sleep
    # TODO: Global variable to store in-game/in-menu status
    logger.info('Entering battle...')
    find_and_click('to_battle')
    time.sleep(0.2)
    pyautogui.press('esc')

    # TODO: Kill status inside loop, global variable?
    # TODO: When spamming activations if none are currently found but in-game status is true keep polling, currently dies when cant find any activations
    while game_status == 1:
        try:
            find_and_click("activate", user_side=True)
            logger.info('ACTIVATE!!!')
        except pyautogui.ImageNotFoundException as e:
            logger.exception("No activations found. Exiting game.")
            # TODO: Don't exit, wait and retry. Also figure out what to do when no longer in game
            sys.exit()

def check_game_status():
    global game_status
    while True:
        try:
            pyautogui.locateOnScreen(f'images/'+device+'/settings.png')
            game_status = 0
            logger.info('Settings found, status = home screen')
        except pyautogui.ImageNotFoundException:
            game_status = 1
            logger.info('Settings not found, status = in game')
            time.sleep(5)

# TODO: How to close this when in another window?
if __name__ == '__main__':
    # Configure and create logger
    logging.basicConfig(filename="gc_bot.log", format='%(asctime)s %(message)s', filemode='w', level=logging.INFO)
    logger = logging.getLogger()

    # Global variable for in-game status. 0 = home screen, 1 = in-game
    game_status = 0
    
    #Setup monitor tread as a daemon so program dies when main threads finished
    game_status_monitor = threading.Thread(target=check_game_status, args=(), daemon=True)
    gameplay_loop = threading.Thread(target=run_game, args=())

    # TODO: Check this out for window handling instead of relying on game icon: https://stackoverflow.com/questions/43785927/python-pyautogui-window-handle
    logger.info('Opening Emulator taskbar icon')
    find_and_click("open_bluestacks")
    time.sleep(0.3)

    logger.info('Starting program...')
    game_status_monitor.start()
    gameplay_loop.start()
