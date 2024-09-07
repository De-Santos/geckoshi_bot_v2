import logging

from aiogram.types import Update
from fastapi import Request, HTTPException, status, FastAPI
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware

import api
import handlers
from bot_starter.same import crate_consumer, shutdown
from variables import bot, dp, WEBHOOK_SECRET, WEBHOOK_PATH, WEB_SERVER_HOST, WEB_SERVER_PORT, WEBHOOK_URL, uvicorn_logging_config

logger = logging.getLogger(__name__)
app = FastAPI()
# Middleware (optional, for example, CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event('startup')
async def on_prod_startup():
    logger.info("Running production startup sequence...")
    await crate_consumer()

    logger.info(f"Setting webhook to {WEBHOOK_URL}{WEBHOOK_PATH}...")
    await bot.set_webhook(f"{WEBHOOK_URL}{WEBHOOK_PATH}", secret_token=WEBHOOK_SECRET)
    logger.info("Webhook set successfully.")


@app.on_event('shutdown')
async def on_prod_shutdown():
    logger.info("Running production shutdown sequence...")
    await shutdown()


@app.post(WEBHOOK_PATH, include_in_schema=False)
async def webhook_handler(request: Request):
    if request.headers.get("X-Telegram-Bot-Api-Secret-Token") != WEBHOOK_SECRET:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    update = Update.model_validate(await request.json(), context={"bot": bot})
    await dp.feed_update(bot=bot, update=update)
    return JSONResponse({"status": "OK"})


# Run the FastAPI server
def prod() -> None:
    logger.info("Setting up production mode...")

    logger.info("Including app routers and setting up production mode...")
    app.include_router(api.base_router)

    logger.info("Including routers and setting up production mode...")
    dp.include_router(handlers.base_router)

    logger.info(f"Starting web server at {WEB_SERVER_HOST}:{WEB_SERVER_PORT}...")
    import uvicorn
    # log_config = uvicorn.config.LOGGING_CONFIG
    # log_config["formatters"]["access"]["fmt"] = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    # log_config["formatters"]["default"]["fmt"] = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    # log_config["handlers"]["default"]["stream"] = "ext://sys.stdout"

    uvicorn.run(app, host=WEB_SERVER_HOST, port=WEB_SERVER_PORT, log_config=uvicorn_logging_config)
