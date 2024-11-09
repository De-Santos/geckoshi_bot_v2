import logging
import os
from io import BytesIO

from aiogram.types import Message

from posts_manager import get_post
from variables import bot

logger = logging.getLogger(__name__)


async def get_post_link() -> dict | None:
    message: Message = await get_post(int(os.getenv('CAPTURED_CHANNEL_ID')))
    if message is None:
        return None
    return {
        "link": f"https://t.me/{message.chat.username}/{message.message_id}",
        "channel": message.chat.model_dump(mode='json'),
    }


async def get_post_photo(resolution: int) -> BytesIO | None:
    message: Message = await get_post(int(os.getenv('CAPTURED_CHANNEL_ID')))
    if message is None or message.photo is None or len(message.photo) == 0:
        return None
    photo_id = message.photo[resolution].file_id
    return await bot.download(photo_id)
