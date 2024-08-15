import uuid

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from database import get_session, TransactionOperation, get_user_balance, SlotsBetHistory, BetType
from filters.base_filters import UserExistsFilter
from keyboard_markup.inline_user_kb import get_slots_menu_kbm, with_step_back_button, get_slots_continue_kbm, with_back_to_menu_button
from lang.lang_based_provider import get_message, format_string
from lang_based_variable import Lang, MessageKey, MenuToSlotsCallback, SlotsPlay, StepBack, InlineKeyboardChange
from slots import play_slots
from states.states import SlotsStates
from transaction_manager import make_transaction_from_system, generate_trace, TraceType

router = Router(name="slots_router")


@router.callback_query(SlotsStates.play, StepBack.filter(), UserExistsFilter())
@router.callback_query(MenuToSlotsCallback.filter(), UserExistsFilter())
async def slots_menu_handler(query: CallbackQuery, lang: Lang, state: FSMContext) -> None:
    await query.message.delete()
    await state.set_state(SlotsStates.enter_amount)
    await query.message.answer(text=get_message(MessageKey.SLOTS_GAME_MENU, lang),
                               reply_markup=get_slots_menu_kbm(lang))


@router.callback_query(SlotsPlay.filter(), SlotsStates.enter_amount, UserExistsFilter())
@router.callback_query(SlotsPlay.filter(), SlotsStates.play, UserExistsFilter())
async def slots_play(query: CallbackQuery, callback_data: SlotsPlay, lang: Lang, state: FSMContext) -> None:
    await state.set_state(SlotsStates.play)
    s = get_session()
    balance = get_user_balance(s, query.from_user.id)
    if balance < callback_data.amount:
        await query.message.answer(text=get_message(MessageKey.SLOTS_NOT_ENOUGH_TO_PLAY, lang),
                                   reply_markup=with_back_to_menu_button(lang, with_step_back_button(lang)))
        return
    trace = uuid.uuid4()
    combination, win_amount, bet_type = play_slots(callback_data.amount)

    operation = TransactionOperation.INCREMENT if bet_type == BetType.WIN else TransactionOperation.DECREMENT
    amount = win_amount if bet_type == BetType.WIN else callback_data.amount
    s.add(SlotsBetHistory(bet_amount=callback_data.amount, win_amount=win_amount, type=bet_type, player_id=query.from_user.id, trace_uuid=trace))
    make_transaction_from_system(query.from_user.id, operation, amount, description="slots play", trace=generate_trace(TraceType.SLOTS_BET, str(trace)), session=s)

    if bet_type == BetType.WIN:
        text = format_string(get_message(MessageKey.SLOTS_WIN, lang), amount=amount, combination=combination)
    else:
        text = format_string(get_message(MessageKey.SLOTS_LOSS, lang), amount=amount, combination=combination)

    await query.message.answer(text=text, reply_markup=with_back_to_menu_button(lang, get_slots_continue_kbm(lang, [{'amount': callback_data.amount}])))


@router.callback_query(InlineKeyboardChange.filter(), SlotsStates.play, UserExistsFilter())
async def change_bet_amount(query: CallbackQuery, lang: Lang) -> None:
    await query.message.edit_reply_markup(reply_markup=get_slots_menu_kbm(lang))
