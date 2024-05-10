import threading
import logging
import time
from gc_utils import Utils
from gc_bot import Bot

device = 'pc'

if __name__ == '__main__':
    logging.basicConfig(filename="gc_bot.log", format='%(asctime)s %(message)s', filemode='w', level=logging.DEBUG)
    logger = logging.getLogger()

    utils = Utils(device, logger)
    bot = Bot(device, utils, logger)

    #Thread to check for 'q' and exit program when pressed to allow user exit
    exit_program = threading.Thread(target=utils.exit_program, args=())
    exit_program.start()

    #Thread to check for gift popup and kill script when found, requires a fix
    gift_popup = threading.Thread(target=utils.gift_popup, args=())
    gift_popup.start()

    #Thread to check for and open cash reward chests
    cash_chest = threading.Thread(target=utils.cash_chest, args=())
    cash_chest.start()

    #Thread to update game status to allow correct behaviour
    status_poller = threading.Thread(target=bot.game_status, args=())
    status_poller.start()

    logger.debug('Opening bluestacks')
    utils.click_image('open_bluestacks')
    time.sleep(0.5)

    #Main gameplay loop, based on game status
    bot.gameplay_loop()