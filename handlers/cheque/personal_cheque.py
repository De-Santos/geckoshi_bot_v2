from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

import cheque
import links
from cheque import ChequeModifier
from database import get_user_balance
from database.enums import ChequeType, SettingsKey, CurrencyType
from filters.base_filters import UserExistsFilter
from keyboard_markup.inline_user_kb import with_step_back_button, get_cheque_action_menu_kbm, get_yes_no_kbm, with_back_to_menu_button, get_cheque_modification_menu_kbm
from lang.lang_based_provider import get_message, format_string
from lang_based_variable import Lang, MessageKey, ChequeMenu, CreateChequeMenu, StepBack, Yes
from providers.tg_arg_provider import ArgType
from settings import get_setting
from states.states import PersonalChequeStates

router = Router(name="personal_cheque")


@router.callback_query(PersonalChequeStates.menu, ChequeMenu.filter(), UserExistsFilter())
@router.callback_query(PersonalChequeStates.amount_require, StepBack.filter(), UserExistsFilter())
async def personal_cheque_menu(query: CallbackQuery, lang: Lang, state: FSMContext) -> None:
    await query.message.delete()
    await state.set_state(PersonalChequeStates.action_menu)
    await state.update_data(cheque_type=ChequeType.PERSONAL.value)
    await query.message.answer(text=get_message(MessageKey.CHEQUE_ACTION_MENU, lang),
                               reply_markup=with_step_back_button(lang, get_cheque_action_menu_kbm(lang, ChequeType.PERSONAL.value)))


@router.callback_query(PersonalChequeStates.action_menu, CreateChequeMenu.filter(), UserExistsFilter())
async def amount_require(query: CallbackQuery, lang: Lang, state: FSMContext) -> None:
    await query.message.delete()
    await _amount_require(query.message, lang, state)


async def _amount_require(message: Message, lang: Lang, state: FSMContext):
    await state.set_state(PersonalChequeStates.amount_require)
    await message.answer(text=get_message(MessageKey.CHEQUE_AMOUNT_REQUIRE, lang),
                         reply_markup=with_step_back_button(lang))


@router.message(PersonalChequeStates.amount_require, UserExistsFilter())
async def amount_handler(message: Message, lang: Lang, state: FSMContext) -> None:
    amount_str = message.text.strip()

    if not amount_str.isdigit():
        await _amount_require(message, lang, state)

    amount = int(amount_str)
    min_gmeme_cheque_amount = await get_setting(SettingsKey.MIN_GMEME_CHEQUE_AMOUNT)
    if amount <= 0 or amount < min_gmeme_cheque_amount:
        await message.answer(text=format_string(get_message(MessageKey.AMOUNT_LESS_THAN_MINIMUM, lang),
                                                amount=min_gmeme_cheque_amount,
                                                currency=CurrencyType.GMEME.name))
        await _amount_require(message, lang, state)
        return

    if await get_user_balance(message.from_user.id) < amount:
        await message.answer(text=get_message(MessageKey.AMOUNT_GREATER_THAN_BALANCE, lang))
        await _amount_require(message, lang, state)
        return

    await state.update_data(amount=amount)
    await review_cheque_amount(message, lang, state)


async def review_cheque_amount(message: Message, lang: Lang, state: FSMContext) -> None:
    await state.set_state(PersonalChequeStates.review_amount)
    data = await state.get_data()

    await message.answer(format_string(get_message(MessageKey.CHEQUE_DATA_CHECK, lang),
                                       amount=data['amount'],
                                       currency=CurrencyType.GMEME.name),
                         reply_markup=with_back_to_menu_button(lang, with_step_back_button(lang, get_yes_no_kbm(lang)), remove_source=True))


@router.callback_query(PersonalChequeStates.review_amount, Yes.filter(), UserExistsFilter())
async def save_cheque(query: CallbackQuery, lang: Lang, state: FSMContext) -> None:
    data = await state.get_data()
    cm: ChequeModifier = await cheque.generate(
        amount=data['amount'],
        creator_id=query.from_user.id,
        type_=ChequeType.PERSONAL,
        currency=CurrencyType.GMEME,
    )
    cheque_link = links.generate(ArgType.CHEQUE, cm.entity.id)
    await query.message.answer(text=format_string(get_message(MessageKey.CHEQUE_SAVED, lang),
                                                  amount=cm.entity.amount,
                                                  currency=cm.entity.currency_type.name,
                                                  cheque_link=cheque_link),
                               reply_markup=get_cheque_modification_menu_kbm(lang, cm.entity.id, cheque_link))
