from aiogram.types import ChatMemberRestricted, ChatMemberMember, ChatMemberAdministrator, ChatMemberOwner

from variables import bot


async def check_membership(tg_user_id: int, url: str) -> bool:
    member = await bot.get_chat_member(chat_id=url, user_id=tg_user_id)
    return member in [ChatMemberOwner, ChatMemberAdministrator, ChatMemberMember, ChatMemberRestricted]
