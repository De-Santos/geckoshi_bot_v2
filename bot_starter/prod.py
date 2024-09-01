from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

import handlers
from bot_starter.same import crate_consumer, shutdown
from variables import bot, dp, WEBHOOK_SECRET, WEBHOOK_PATH, WEB_SERVER_HOST, WEB_SERVER_PORT, WEBHOOK_URL
from .log import logger


def prod() -> None:
    logger.info("Setting up production mode...")
    app = web.Application()

    logger.info("Registering startup and shutdown handlers...")
    dp.startup.register(on_prod_startup)
    dp.shutdown.register(on_prod_shutdown)

    logger.info("Including routers and setting up development mode...")
    dp.include_router(handlers.base_router)

    logger.info("Setting up webhook request handler...")
    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
        secret_token=WEBHOOK_SECRET,
    )
    webhook_requests_handler.register(app, path=WEBHOOK_PATH)

    logger.info("Setting up application with dispatcher hooks...")
    setup_application(app, dp, bot=bot)

    logger.info(f"Starting web server at {WEB_SERVER_HOST}:{WEB_SERVER_PORT}...")
    try:
        web.run_app(app, host=WEB_SERVER_HOST, port=WEB_SERVER_PORT)
    except Exception as e:
        logger.error(f"Failed to start the web server: {e}")
        raise


async def on_prod_startup() -> None:
    await crate_consumer()

    logger.info(f"Setting webhook to {WEBHOOK_URL}{WEBHOOK_PATH}...")
    await bot.set_webhook(f"{WEBHOOK_URL}{WEBHOOK_PATH}", secret_token=WEBHOOK_SECRET)
    logger.info("Webhook set successfully.")


async def on_prod_shutdown() -> None:
    logger.info("Running production shutdown sequence...")
    await shutdown()
