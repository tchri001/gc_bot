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

    exit_program = threading.Thread(target=utils.exit_program, args=())
    exit_program.start()

    status_poller = threading.Thread(target=bot.game_status, args=())
    status_poller.start()

    logger.debug('Opening bluestacks')
    utils.click_image('open_bluestacks')
    time.sleep(0.5)

    bot.gameplay_loop()