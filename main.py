import asyncio
import logging
import sys

import handlers
from database import init_db, get_session, Setting, SettingsKey
from kafka_processor import Topic
from message_processor.executor import message_elevator_thread_launcher
from message_processor.handlers import message_observer
from protobuf import message_pb2
from variables import bot, dp, redis


async def main() -> None:
    await bot.delete_webhook(drop_pending_updates=True)
    dp.include_router(handlers.base_router)
    await redis.flushall()
    # message_elevator_thread_launcher(asyncio.get_event_loop(), Topic.MESSAGE, message_pb2.Message, message_observer)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    init_db()
    asyncio.run(main())
