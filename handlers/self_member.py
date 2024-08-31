import logging

from aiogram import Router, types, Bot
from aiogram.enums import ChatType

from database import get_admin_ids

router = Router(name="bot_router")

logger = logging.getLogger(__name__)


async def notify_admins(bot: Bot, message: str) -> None:
    for i in await get_admin_ids():
        try:
            await bot.send_message(chat_id=i, text=message)
        except Exception as e:
            logger.error("An exception occurred while notifying admin id: %s, with message: %s, Error: %s", i, message, str(e))


@router.my_chat_member()
async def handle_bot_added_to_chat(event: types.ChatMemberUpdated, bot: Bot):
    if event.new_chat_member.user.id != bot.id:
        return

    chat = event.chat
    chat_type = chat.type
    chat_id = chat.id

    if event.new_chat_member.status in {'member', 'administrator'}:
        if chat_type in {ChatType.GROUP, ChatType.SUPERGROUP, ChatType.CHANNEL}:
            chat_type_name = "group" if chat_type in {ChatType.GROUP, ChatType.SUPERGROUP} else "channel"
            chat_privacy = "public" if chat.username else "private"
            message = f"Bot added to a {chat_privacy} {chat_type_name}: {chat.title} by <a href=\"tg://user?id={event.from_user.id}\">{event.from_user.first_name}</a>\n\nchat_id: <code>{chat_id}</code>"
            logger.info(f"Bot added to {chat_type}:{chat_id} as {event.new_chat_member.status}, chat privacy: {chat_privacy}")
            await notify_admins(bot, message)
