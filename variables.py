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

# build mode
MODE = os.getenv('MODE')

# bot
redis = Redis.from_url(url=os.getenv('REDIS_URL'))
storage = RedisStorage(redis)
dp = Dispatcher(storage=storage)
bot: Bot = Bot(token=os.getenv('API_TOKEN'), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
bot_url: str = os.getenv('BOT_URL')
start_time = datetime.datetime.now()

# web server settings
WEB_SERVER_HOST = os.getenv('WEB_SERVER_HOST')
WEB_SERVER_PORT = int(os.getenv('WEB_SERVER_PORT'))

# bot webhook settings
WEBHOOK_URL = os.getenv('WEBHOOK_URL')
WEBHOOK_PATH = os.getenv('WEBHOOK_PATH', "/webhook")
WEBHOOK_SECRET = os.getenv('WEBHOOK_SECRET')

# captcha
captcha_val_set = (string.ascii_uppercase + string.digits)
captcha_length = int(os.getenv('CAPTCHA_LENGTH'))
captcha_answer_list_size = int(os.getenv('CAPTCHA_ANSWER_LIST_SIZE', 3))
captcha_complexity_level = int(os.getenv('CAPTCHA_COMPLEXITY'))

# log lower levels to stdout
stdout_handler = logging.StreamHandler(stream=sys.stdout)
stdout_handler.addFilter(lambda rec: rec.levelno <= logging.INFO)

# log higher levels to stderr (red)
stderr_handler = logging.StreamHandler(stream=sys.stderr)
stderr_handler.addFilter(lambda rec: rec.levelno > logging.INFO)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
    handlers=[stdout_handler, stderr_handler]
)

uvicorn_logging_config: dict = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": "%(asctime)s - %(levelprefix)s %(message)s",
            "use_colors": None,
        },
        "access": {
            "()": "uvicorn.logging.AccessFormatter",
            "fmt": '%(asctime)s - %(levelprefix)s %(client_addr)s - "%(request_line)s" %(status_code)s',  # noqa: E501
        },
    },
    "handlers": {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
        "access": {
            "formatter": "access",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
        "error": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "stream": "ext://sys.stderr",
        },
    },
    "loggers": {
        "uvicorn": {"handlers": ["default"], "level": "INFO", "propagate": False},
        "uvicorn.error": {"handlers": ["error"], "level": "ERROR", "propagate": False},
        "uvicorn.access": {"handlers": ["access"], "level": "INFO", "propagate": False},
    },
}
