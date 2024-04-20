import numpy as np
import pyautogui
import time
import threading
import sys, os
import logging
from utility import *

# Icons don't work across device so change this as needed
#device = 'laptop'
device = 'pc'

# Enter into a battle
def enter_game():
    logger.info('Entering battle...')
    find_and_click('to_battle')
    time.sleep(0.2)
    pyautogui.press('esc')
    run_game()

# Spam abilities whilst in game
def run_game():
    global game_status
    
    while game_status == 1:
        try:
            #TODO: Check if the locate on screen uses greyscale, extend icon to right side of bar to show full charge
            find_and_click("activate", user_side=True)
            logger.info('ACTIVATE!!!')
        except pyautogui.ImageNotFoundException as e:
            time.sleep(1)
            logger.info('Waiting for refresh')

def check_game_status():
    global game_status
    while True:
        try:
            pyautogui.locateOnScreen(f'images/'+device+'/settings.png')
            game_status = 0
            logger.info('Settings found, status = home screen')
            enter_game()
        #TODO: I don't think this is working
        except pyautogui.ImageNotFoundException: 
            game_status = 1
            logger.info('Settings not found, status = in game')
            time.sleep(1)

if __name__ == '__main__':
    # Configure and create logger
    logging.basicConfig(filename="gc_bot.log", format='%(asctime)s %(message)s', filemode='w', level=logging.INFO)
    logger = logging.getLogger()

    # Start up exit on input thread
    exit_program = threading.Thread(target=user_exit, args=(logger,))
    exit_program.start()

    # Global variable for in-game status where 0 = home screen and 1 = in-game
    game_status = 0
    
    # Setup threads, game status keeps the var updated and gameplay does the actual interaction
    game_status_monitor = threading.Thread(target=check_game_status, args=())
    gameplay_loop = threading.Thread(target=run_game, args=())

    # Open up the game then start 
    # TODO: Check this out for window handling instead of relying on game icon: https://stackoverflow.com/questions/43785927/python-pyautogui-window-handle
    logger.info('Opening Emulator taskbar icon')
    find_and_click("open_bluestacks")
    time.sleep(0.5)

    # Start both threads to kick off playing
    logger.info('Starting program...')
    game_status_monitor.start()
    #enter_game()