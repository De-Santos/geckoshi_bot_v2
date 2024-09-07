import asyncio
from typing import Literal

from .dev import dev
from .log import logger
from .prod import prod

Mode = Literal['dev', 'prod']


def start(mode: Mode) -> None:
    logger.info(f"Starting bot in {mode} mode...")
    if mode == 'dev':
        asyncio.run(dev())
    elif mode == 'prod':
        prod()
    else:
        logger.error(f"Invalid mode provided: {mode}")
        raise ValueError(f"Invalid mode: {mode}")
