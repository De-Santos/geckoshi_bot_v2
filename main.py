import logging

import bot_starter
from variables import stdout_handler, stderr_handler, MODE

if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
        handlers=[stdout_handler, stderr_handler]
    )
    bot_starter.start(MODE)
