import os

from aiogram import Router, F
from aiogram.types import Message

from filters.base_filters import ChannelIdFilter
from posts_manager import cache_post

router = Router(name="channel_router")

router.message.filter(ChannelIdFilter(int(os.getenv('CAPTURED_CHANNEL_ID'))))


async def _cache_post(message: Message) -> None:
    await cache_post(int(os.getenv('CAPTURED_CHANNEL_ID')), message)


@router.message(F.photo)
async def new_photo_post_handler(message: Message) -> None:
    await _cache_post(message)


@router.message()
async def new_post_handler(message: Message) -> None:
    await _cache_post(message)
