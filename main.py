import asyncio
import time
import logging

from get_chats.parsing_chats import main
if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')

    logger.info('Starting parser')
    try:
        asyncio.run(main())
    except Exception as ex:
        print('ERROR', ex)
    while True: time.sleep(5000)