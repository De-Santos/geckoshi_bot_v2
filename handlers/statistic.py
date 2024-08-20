from aiogram import Router
from aiogram.types import CallbackQuery

from database import get_session, get_users_statistic
from filters.base_filters import UserExistsFilter
from keyboard_markup.inline_user_kb import with_back_to_menu_button
from lang.lang_based_provider import Lang, get_message, format_string
from lang_based_variable import MessageKey, MenuToStatistic

router = Router(name="statistic_router")


@router.callback_query(MenuToStatistic.filter(), UserExistsFilter())
async def process_statistic(query: CallbackQuery, lang: Lang) -> None:
    await query.message.delete()
    today_count, total_count = await get_users_statistic(get_session())
    await query.message.answer(text=format_string(get_message(MessageKey.PUBLIC_STATISTIC, lang),
                                                  total_users=total_count,
                                                  today_joined=today_count),
                               reply_markup=with_back_to_menu_button(lang, remove_source=True))
