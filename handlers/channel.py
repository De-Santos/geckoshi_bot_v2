import logging
import os

from aiogram import Router
from aiogram.types import Message

from filters.base_filters import ChannelIdFilter
from posts_manager import cache_post

router = Router(name="channel_router")
logger = logging.getLogger(__name__)

captured_channel_id = int(os.getenv('CAPTURED_CHANNEL_ID'))
logger.info(f"Setting up filter for channel ID: {captured_channel_id}")

router.channel_post.filter(ChannelIdFilter(captured_channel_id))


async def _cache_post(message: Message) -> None:
    try:
        logger.info(f"Caching post with ID: {message.message_id} from channel ID: {captured_channel_id}")
        await cache_post(captured_channel_id, message)
        logger.info(f"Successfully cached post with ID: {message.message_id}")
    except Exception as e:
        logger.error(f"Failed to cache post with ID: {message.message_id}", exc_info=e)


@router.channel_post()
async def new_post_handler(message: Message) -> None:
    logger.info(f"New post received from channel ID: {message.chat.id}, post ID: {message.message_id}")
    await _cache_post(message)
