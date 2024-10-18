import asyncio

from rabbit import MessageConsumerRunner
from singleton import GlobalContext
from variables import bot
from .log import logger


async def crate_consumer():
    logger.info("Starting message consumer runner...")
    # gb = GlobalContext()
    # gb.message_consumer_runner = MessageConsumerRunner(asyncio.get_event_loop())
    # gb.message_consumer_runner.run()


async def shutdown() -> None:
    logger.info("Shutting down message consumer runner...")
    gb = GlobalContext()
    if gb.message_consumer_runner:
        gb.message_consumer_runner.stop()

    logger.info("Removing webhook and cleaning up...")
    await bot.delete_webhook(drop_pending_updates=True)
    logger.info("Shutdown complete.")
