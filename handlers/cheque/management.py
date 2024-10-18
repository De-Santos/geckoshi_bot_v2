from typing import Optional

from aiogram import Router, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, User, ChatFullInfo, MessageOriginUser
from mako.exceptions import RuntimeException

import cheque
import links
from cheque import ChequeModifier
from filters.base_filters import UserExistsFilter
from keyboard_markup.inline_user_kb import with_back_to_menu_button, get_cheque_modification_menu_kbm, with_step_back_button, get_cheque_already_linked_to_user_menu_kbm
from lang.lang_based_provider import get_message, format_string
from lang_based_variable import Lang, AddDescriptionToCheque, MessageKey, ChequeModifiableView, LinkChequeToUser
from providers.tg_arg_provider import ArgType
from states.states import ChequeModifyingStates
from utils.aiogram import extract_message

router = Router(name="management_cheque")


@router.callback_query(ChequeModifiableView.filter(), UserExistsFilter())
async def cheque_modifiable_view(qm: CallbackQuery | Message, callback_data: ChequeModifiableView, lang: Lang) -> None:
    message = extract_message(qm)
    cm: Optional[ChequeModifier] = await cheque.get_active(callback_data.cheque_id)
    if cm is None:
        await message.answer(text=get_message(MessageKey.CHEQUE_NOT_FOUND, lang),
                             reply_markup=with_back_to_menu_button(lang))
        return
    cheque_link = links.generate(ArgType.CHEQUE, cm.entity.id)
    await message.answer(text=format_string(get_message(MessageKey.CHEQUE_SAVED, lang),
                                            amount=cm.entity.amount,
                                            currency=cm.entity.currency_type.name,
                                            cheque_link=cheque_link),
                         reply_markup=get_cheque_modification_menu_kbm(lang, cm.entity.id, cheque_link))


@router.callback_query(AddDescriptionToCheque.filter(), UserExistsFilter())
async def add_description_to_cheque(query: CallbackQuery, callback_data: AddDescriptionToCheque, lang: Lang, state: FSMContext) -> None:
    await state.set_state(ChequeModifyingStates.add_description)
    await state.update_data(cheque_id=callback_data.cheque_id)
    await query.message.answer(text=get_message(MessageKey.REQUEST_CHEQUE_DESCRIPTION, lang),
                               reply_markup=with_step_back_button(lang))


@router.message(ChequeModifyingStates.add_description, UserExistsFilter())
async def save_description(message: Message, lang: Lang, state: FSMContext) -> None:
    cheque_id = (await state.get_data()).get('cheque_id')
    cm: Optional[ChequeModifier] = await cheque.get_active(cheque_id)
    if cm is None:
        await message.answer(text=get_message(MessageKey.CHEQUE_IS_NOT_MODIFIABLE, lang),
                             reply_markup=with_back_to_menu_button(lang))
        return
    else:
        await cm.update_description(description=message.html_text)
        await message.answer(text=get_message(MessageKey.CHEQUE_MODIFIED_SUCCESSFULLY, lang))
        await cheque_modifiable_view(message, ChequeModifiableView(cheque_id=cm.entity.id), lang)


@router.callback_query(LinkChequeToUser.filter(), UserExistsFilter())
async def link_cheque_to_user(query: CallbackQuery, callback_data: LinkChequeToUser, lang: Lang, state: FSMContext, bot: Bot) -> None:
    await state.set_state(ChequeModifyingStates.link_to_user)
    cm: Optional[ChequeModifier] = await cheque.get_active(callback_data.cheque_id)
    if cm is None:
        await query.message.answer(text=get_message(MessageKey.CHEQUE_IS_NOT_MODIFIABLE, lang),
                                   reply_markup=with_back_to_menu_button(lang))
        return

    if cm.entity.connected_to_user is not None and callback_data.override is not True:
        await query.message.answer(text=format_string(get_message(MessageKey.CHEQUE_ALREADY_LINKED_TO_USER, lang),
                                                      username=(await bot.get_chat(cm.entity.connected_to_user)).username),
                                   reply_markup=with_step_back_button(lang, get_cheque_already_linked_to_user_menu_kbm(lang, callback_data.cheque_id)))
        return

    await state.update_data(cheque_id=callback_data.cheque_id)
    await query.message.answer(text=get_message(MessageKey.REQUEST_CHEQUE_LINK_USER, lang),
                               reply_markup=with_step_back_button(lang))


@router.message(ChequeModifyingStates.link_to_user, UserExistsFilter())
async def process_link_cheque_to_user(message: Message, lang: Lang, state: FSMContext, bot: Bot) -> None:
    cheque_id = (await state.get_data()).get('cheque_id')
    cm: Optional[ChequeModifier] = await cheque.get_active(cheque_id)
    linked_user: User | ChatFullInfo | None = None
    if cm is None:
        await message.answer(text=get_message(MessageKey.CHEQUE_IS_NOT_MODIFIABLE, lang),
                             reply_markup=with_back_to_menu_button(lang))
        return

    if message.forward_origin is not None and isinstance(message.forward_origin, MessageOriginUser):
        await cm.link_user(message.forward_origin.sender_user.id)
        linked_user = message.forward_origin.sender_user
    elif message.text and message.text.startswith('@'):
        username = message.text.strip()
        try:
            linked_user = await bot.get_chat(username)
            user_id = linked_user.id
            await message.reply(f"The user's ID for {username} is: {user_id}")
        except RuntimeException as _:
            await message.reply(text=format_string(get_message(MessageKey.FAILED_TO_FIND_THE_USER, lang), username=username),
                                reply_markup=with_back_to_menu_button(lang))
    else:
        await message.delete()
        await message.answer(text=get_message(MessageKey.REQUEST_CHEQUE_LINK_USER, lang),
                             reply_markup=with_step_back_button(lang))
        return

    await cm.link_user(linked_user.id)
    await message.answer(text=format_string(get_message(MessageKey.CHEQUE_LINKED_TO_USER_SUCCESSFULLY, lang), username=linked_user.username))
    await cheque_modifiable_view(message, ChequeModifiableView(cheque_id=cm.entity.id), lang)
