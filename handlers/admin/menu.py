from datetime import datetime

import humanfriendly
from aiogram import Router, F
from aiogram.types import Message

from database import get_verified_user_count, get_session
from filters.base_filters import UserExistsFilter
from keyboard_markup.inline_user_kb import get_admin_menu_kbm
from lang.lang_based_provider import get_message, format_string
from lang_based_variable import Lang, MessageKey
from variables import start_time

router = Router(name="admin_menu_router")


def calculate_uptime() -> str:
    current_time = datetime.now()
    uptime_duration = current_time - start_time
    uptime_seconds = int(uptime_duration.total_seconds())
    return humanfriendly.format_timespan(uptime_seconds)


@router.message(F.text == "/admin_panel", UserExistsFilter())
async def admin_menu_handler(message: Message, lang: Lang) -> None:
    await message.delete()
    await message.answer(text=format_string(get_message(MessageKey.ADMIN_PANEL, lang),
                                            uptime=calculate_uptime(),
                                            user_count=await get_verified_user_count(get_session())),
                         reply_markup=get_admin_menu_kbm(lang))
