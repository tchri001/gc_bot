import pyautogui
import sys, os
import time
import keyboard
import threading
import logging
from pynput.mouse import Listener, Button

def on_click(x, y, button, pressed):
    if pressed and button == Button.left:
        logger.info(f'x={x} and y={y}')

def mark_boundary():
    while True:
        if keyboard.is_pressed('s'):
            logger.info('Recording boundaries')
            time.sleep(1)
        if keyboard.is_pressed('e'):
            logger.info('Ending boundaries')
            time.sleep(1)

def user_exit():
    while True:
        if keyboard.is_pressed('q'):
            logger.info('End program')
            os._exit(1) 

if __name__ == '__main__':
    exit_program = threading.Thread(target=user_exit, args=())
    exit_program.start()

    log_marker = threading.Thread(target=mark_boundary, args=())
    log_marker.start()

    logging.basicConfig(filename="mouse_coords.log", format='%(asctime)s %(message)s', filemode='w', level=logging.INFO)
    logger = logging.getLogger()

    with Listener(on_click=on_click) as listener:
        listener.join()