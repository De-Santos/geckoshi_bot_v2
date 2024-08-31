import asyncio
import logging

import handlers
from database import init_db
from rabbit import MessageConsumerRunner
from variables import bot, dp, stdout_handler, stderr_handler


async def main() -> None:
    await init_db()
    await bot.delete_webhook(drop_pending_updates=True)
    dp.include_router(handlers.base_router)
    MessageConsumerRunner(asyncio.get_event_loop()).run()
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(name)s - Thread: %(threadName)s - %(message)s',
        handlers=[stdout_handler, stderr_handler]
    )
    asyncio.run(main())
