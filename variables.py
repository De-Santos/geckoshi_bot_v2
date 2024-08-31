import datetime
import logging
import os
import string
import sys

from aiogram import Bot
from aiogram import Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage
from dotenv import load_dotenv
from redis.asyncio import Redis

load_dotenv()
redis = Redis.from_url(url=os.getenv('REDIS_URL'))
storage = RedisStorage(redis)
dp = Dispatcher(storage=storage)
bot: Bot = Bot(token=os.getenv('API_TOKEN'), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
start_time = datetime.datetime.now()

# log lower levels to stdout
stdout_handler = logging.StreamHandler(stream=sys.stdout)
stdout_handler.addFilter(lambda rec: rec.levelno <= logging.INFO)

# log higher levels to stderr (red)
stderr_handler = logging.StreamHandler(stream=sys.stderr)
stderr_handler.addFilter(lambda rec: rec.levelno > logging.INFO)

# captcha
captcha_val_set = (string.ascii_uppercase + string.digits)
captcha_length = int(os.getenv('CAPTCHA_LENGTH'))
captcha_answer_list_size = int(os.getenv('CAPTCHA_ANSWER_LIST_SIZE', 3))
captcha_complexity_level = int(os.getenv('CAPTCHA_COMPLEXITY'))
