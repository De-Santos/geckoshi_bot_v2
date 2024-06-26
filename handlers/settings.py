from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from callbacks.start import LangSetCallback
from database import get_session, update_user_language
from filters.base_filters import UserExistsFilter, ChatTypeFilter
from lang.lang_based_text_provider import MessageKey
from lang.lang_based_text_provider import get_message
from lang.lang_provider import cache_lang
from states.settings import SettingsStates

router = Router(name="start_router")

router.message.filter(ChatTypeFilter())
router.callback_query.filter(ChatTypeFilter())


@router.callback_query(UserExistsFilter(), LangSetCallback.filter(), SettingsStates.language)
async def change_lang_handler(query: CallbackQuery, callback_data: LangSetCallback, state: FSMContext) -> None:
    session = get_session()
    update_user_language(session, query.from_user.id, callback_data.lang)
    await query.answer(text=get_message(MessageKey.lANG_CHANGE, callback_data.lang))
    await cache_lang(query.from_user.id, callback_data.lang)
    await state.clear()
