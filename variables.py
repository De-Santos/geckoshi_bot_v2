import datetime
import os

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
