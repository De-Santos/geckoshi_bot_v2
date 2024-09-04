from contextlib import asynccontextmanager

from aiogram.types import Update
from fastapi import FastAPI, Request, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

import handlers
from bot_starter.same import crate_consumer, shutdown
from variables import bot, dp, WEBHOOK_SECRET, WEBHOOK_PATH, WEB_SERVER_HOST, WEB_SERVER_PORT, WEBHOOK_URL
from .log import logger


@asynccontextmanager
async def lifespan(_: FastAPI):
    await on_prod_startup()
    yield
    await shutdown()


app = FastAPI(lifespan=lifespan)

# Middleware (optional, for example, CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def on_prod_startup():
    logger.info("Running production startup sequence...")
    await crate_consumer()

    logger.info(f"Setting webhook to {WEBHOOK_URL}{WEBHOOK_PATH}...")
    await bot.set_webhook(f"{WEBHOOK_URL}{WEBHOOK_PATH}", secret_token=WEBHOOK_SECRET)
    logger.info("Webhook set successfully.")


async def on_prod_shutdown():
    logger.info("Running production shutdown sequence...")
    await shutdown()


@app.post(WEBHOOK_PATH)
async def webhook_handler(request: Request):
    if request.headers.get("X-Telegram-Bot-Api-Secret-Token") != WEBHOOK_SECRET:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    update = Update.model_validate(await request.json(), context={"bot": bot})
    await dp.feed_update(bot=bot, update=update)
    return JSONResponse({"status": "OK"})


# Run the FastAPI server
def prod() -> None:
    logger.info("Setting up production mode...")

    logger.info("Including routers and setting up production mode...")
    dp.include_router(handlers.base_router)

    logger.info(f"Starting web server at {WEB_SERVER_HOST}:{WEB_SERVER_PORT}...")
    import uvicorn
    log_config = uvicorn.config.LOGGING_CONFIG
    log_config["formatters"]["access"]["fmt"] = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    log_config["formatters"]["default"]["fmt"] = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    log_config["handlers"]["default"]["stream"] = "ext://sys.stdout"

    uvicorn.run(app, host=WEB_SERVER_HOST, port=WEB_SERVER_PORT, log_config=log_config)
