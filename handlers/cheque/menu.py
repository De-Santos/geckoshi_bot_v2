from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from filters.base_filters import UserExistsFilter
from keyboard_markup.inline_user_kb import get_public_cheque_menu_kbm, with_back_to_menu_button
from lang.lang_based_provider import get_message
from lang_based_variable import MenuToChequeCallback, Lang, MessageKey, StepBack
from states.states import PersonalChequeStates

router = Router(name="cheque_menu")


@router.callback_query(StepBack.filter(), UserExistsFilter())
@router.callback_query(MenuToChequeCallback.filter(), UserExistsFilter())
async def cheque_menu_handler(query: CallbackQuery, lang: Lang, state: FSMContext) -> None:
    await query.message.delete()
    await state.set_state(PersonalChequeStates.menu)
    await query.message.answer(text=get_message(MessageKey.CHEQUE_MENU, lang),
                               reply_markup=with_back_to_menu_button(lang, get_public_cheque_menu_kbm(lang), remove_source=True))
