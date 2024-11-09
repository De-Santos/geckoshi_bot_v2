import asyncio
import logging
from typing import Union

from aiogram.enums import ChatMemberStatus

from variables import bot

logger = logging.getLogger(__name__)


async def check_membership(tg_user_id: int, chat_id: str | int) -> bool:
    member = await bot.get_chat_member(chat_id=chat_id, user_id=tg_user_id)
    return member.status in [ChatMemberStatus.CREATOR,
                             ChatMemberStatus.ADMINISTRATOR,
                             ChatMemberStatus.MEMBER,
                             ChatMemberStatus.RESTRICTED]


async def check_memberships(tg_user_id: int, chat_ids: list[str | int]) -> bool:
    # Create tasks for each membership check and gather them in parallel
    try:
        results = await asyncio.gather(*[check_membership(tg_user_id, chat_id) for chat_id in chat_ids])
    except Exception as e:
        logger.error(f"Error while checking memberships: {e}")
        return False

    # Return True only if all results are True (user is a member of all chat_ids)
    return all(results)


async def validate_bot_in_chats(chat_id: Union[str, int]) -> bool:
    try:
        bot_member = await bot.get_chat_member(chat_id, bot.id)
        bot_has_access = bot_member.status in [ChatMemberStatus.ADMINISTRATOR,
                                               ChatMemberStatus.MEMBER,
                                               ChatMemberStatus.RESTRICTED]

        return bot_has_access
    except Exception as e:
        logger.error(f"Error checking chat {chat_id}: {e}")
        return False
