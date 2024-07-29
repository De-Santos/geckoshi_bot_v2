from aiogram.enums import ChatMemberStatus

from variables import bot


async def check_membership(tg_user_id: int, chat_id: str | int) -> bool:
    member = await bot.get_chat_member(chat_id=chat_id, user_id=tg_user_id)
    return member.status in [ChatMemberStatus.CREATOR,
                             ChatMemberStatus.ADMINISTRATOR,
                             ChatMemberStatus.MEMBER,
                             ChatMemberStatus.RESTRICTED]
