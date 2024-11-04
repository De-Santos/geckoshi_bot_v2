import asyncio

from rabbit import MessageConsumerRunner
from rabbit.consumer_runners import PersonalChequeActivationConsumerRunner
from singleton import GlobalContext
from variables import bot
from .log import logger


async def crate_consumer():
    logger.info("Starting rabbit consumers...")
    gb = GlobalContext()
    gb.message_consumer_runner = MessageConsumerRunner(asyncio.get_event_loop())
    gb.personal_cheque_activation_consumer_runner = PersonalChequeActivationConsumerRunner(asyncio.get_event_loop())
    gb.message_consumer_runner.run()
    gb.personal_cheque_activation_consumer_runner.run()


async def shutdown() -> None:
    logger.info("Shutting down rabbit consumers...")
    gb = GlobalContext()
    if gb.message_consumer_runner:
        gb.message_consumer_runner.stop()

    if gb.personal_cheque_activation_consumer_runner:
        gb.personal_cheque_activation_consumer_runner.stop()

    logger.info("Removing webhook and cleaning up...")
    await bot.delete_webhook(drop_pending_updates=True)
    logger.info("Shutdown complete.")
