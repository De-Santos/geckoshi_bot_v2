from aiogram.enums import ChatMemberStatus

from variables import bot


async def check_membership(tg_user_id: int, chat_id: str | int) -> bool:
    member = await bot.get_chat_member(chat_id=chat_id, user_id=tg_user_id)
    return member.status in [ChatMemberStatus.CREATOR,
                             ChatMemberStatus.ADMINISTRATOR,
                             ChatMemberStatus.MEMBER,
                             ChatMemberStatus.RESTRICTED]


async def check_memberships(tg_user_id: int, chat_ids: list[str | int]) -> bool:
    for chat_id in chat_ids:
        is_member = await check_membership(tg_user_id, chat_id)
        if not is_member:
            return False

    return True
