import asyncio
import logging
from typing import Union

from aiogram.enums import ChatMemberStatus

from variables import bot

logger = logging.getLogger(__name__)


async def check_membership(tg_user_id: int, chat_id: str | int) -> bool:
    try:
        member = await bot.get_chat_member(chat_id=chat_id, user_id=tg_user_id)
        return member.status in [
            ChatMemberStatus.CREATOR,
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.MEMBER,
            ChatMemberStatus.RESTRICTED,
        ]
    except Exception as e:
        logger.error(f"Error while checking membership for chat {chat_id}: {e}")
        return False


async def check_memberships(tg_user_id: int, chat_ids: list[str | int], return_info: bool = False) -> bool | dict[int | str, bool]:
    results_map = {}

    try:
        # Create tasks for each membership check and gather them in parallel
        results = await asyncio.gather(*[check_membership(tg_user_id, chat_id) for chat_id in chat_ids])
        results_map.update({chat_id: result for chat_id, result in zip(chat_ids, results)})
    except Exception as e:
        logger.error(f"Error while checking memberships: {e}")
        results_map = {chat_id: False for chat_id in chat_ids}

    # If return_info is True, return the results map
    if return_info:
        return results_map

    # Otherwise, return True only if the user is a member of all chats
    return all(results_map.values())


async def validate_bot_in_chats(chat_id: Union[str, int]) -> bool:
    try:
        bot_member = await bot.get_chat_member(chat_id, bot.id)
        bot_has_access = bot_member.status in [ChatMemberStatus.ADMINISTRATOR,
                                               ChatMemberStatus.RESTRICTED]

        return bot_has_access
    except Exception as e:
        logger.error(f"Error checking chat {chat_id}: {e}")
        return False


async def check_bot_in_chats(chat_ids: list[str]) -> bool:
    # Create tasks for each chat check and gather them in parallel
    try:
        results = await asyncio.gather(*[validate_bot_in_chats(chat_id) for chat_id in chat_ids])
    except Exception as e:
        logger.error(f"Error while checking memberships: {e}")
        return False

    return all(results)
