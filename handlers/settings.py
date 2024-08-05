from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from database import get_session, update_user_language
from filters.base_filters import UserExistsFilter
from keyboard_markup.inline_user_kb import get_lang_kbm, with_exit_button
from lang.lang_based_provider import MessageKey
from lang.lang_based_provider import get_message
from lang.lang_provider import cache_lang
from lang_based_variable import LangSetCallback, SetLangMenu, Lang
from states.settings import SettingsStates

router = Router(name="settings_router")


@router.callback_query(SetLangMenu.filter(), UserExistsFilter())
async def settings_set_lang_menu(query: CallbackQuery, lang: Lang, state: FSMContext) -> None:
    await state.set_state(SettingsStates.language)
    await query.message.answer(text=get_message(MessageKey.LANG_MENU, lang),
                               reply_markup=with_exit_button(lang, get_lang_kbm()))


@router.callback_query(LangSetCallback.filter(), SettingsStates.language, UserExistsFilter())
async def change_lang_handler(query: CallbackQuery, callback_data: LangSetCallback, state: FSMContext) -> None:
    session = get_session()
    update_user_language(session, query.from_user.id, callback_data.lang)
    await query.answer(text=get_message(MessageKey.LANG_CHANGE, callback_data.lang))
    await cache_lang(query.from_user.id, callback_data.lang)
    await query.message.delete()
    await state.clear()
