import logging
from io import BytesIO
from typing import Optional

from aiogram.types import ChatFullInfo

import cache
import chat_processor
from chat_processor.member import validate_bot_in_chats
from variables import bot

logger = logging.getLogger(__name__)


async def __get_chat_safe(chat_id: int | str) -> Optional[ChatFullInfo]:
    try:
        return await bot.get_chat(chat_id)
    except BaseException as e:
        logger.warning(f"Error while getting chat {chat_id} : {e}")
        return None


async def get_chat_full_info_impl(chat_id: int | str) -> dict:
    try:
        data = None
        has_access = False
        cfi: Optional[ChatFullInfo] = await __get_chat_safe(chat_id)
        if cfi is not None:
            data = cfi.model_dump(mode='json', exclude={'pinned_message', 'available_reactions'})
            has_access = await validate_bot_in_chats(cfi.id)

        return {
            'has_access': has_access,
            'data': data,
        }
    except BaseException as e:
        logger.error(f"Error while getting chat full info: {e}")
        raise e


@cache.cacheable(ttl="1h", save_as_blob=True, cache_result_ignore_val=None)
async def get_chat_img_impl(file_id: str) -> BytesIO | None:
    try:
        return await chat_processor.get_chat_img(file_id)
    except BaseException as e:
        logger.error(f"Error while downloading chat img: {e}")
        return None
