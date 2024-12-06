import handlers
from bot_starter.same import crate_consumer, shutdown
from variables import bot, dp
from .log import logger


async def dev() -> None:
    # logger.info("Initializing database...")
    # await init_db()
    # logger.info("Database initialized successfully.")

    logger.info("Removing existing webhook (if any) and dropping pending updates...")
    await bot.delete_webhook(drop_pending_updates=True)

    logger.info("Including routers and setting up development mode...")
    dp.include_router(handlers.base_router)
    dp.include_router(handlers.custom_router)

    await crate_consumer()

    try:
        logger.info("Starting polling...")
        await dp.start_polling(bot)
    finally:
        logger.info("Shutting down...")
        await shutdown()
