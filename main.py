import asyncio
import logging

import handlers
from database import init_db
from message_processor.executor import message_elevator_thread_launcher
from rabbit import ReconnectingMessageConsumer
from variables import bot, dp, redis


async def main() -> None:
    await bot.delete_webhook(drop_pending_updates=True)
    dp.include_router(handlers.base_router)
    # await redis.flushall()
    message_elevator_thread_launcher(ReconnectingMessageConsumer(asyncio.get_event_loop()))
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - Thread: %(threadName)s - %(message)s',
        handlers=[
            logging.StreamHandler()
        ]
    )
    init_db()
    asyncio.run(main())
