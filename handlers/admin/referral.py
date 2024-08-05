from datetime import datetime, timedelta

from aiogram import Router, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from database import get_session, get_top_users_by_referrals, get_top_users_by_referrals_with_start_date, SettingsKey
from filters.base_filters import UserExistsFilter
from keyboard_markup.inline_user_kb import with_exit_button
from lang.lang_based_provider import format_string, get_message
from lang_based_variable import RefTop, ChangeRefPay, Lang, MessageKey
from settings import get_setting
from settings.settings_manager import update_setting
from states.settings import SettingsStates

router = Router(name="referral_router")


@router.callback_query(RefTop.filter(), UserExistsFilter())
async def ref_top_handler(query: CallbackQuery, callback_data: RefTop, bot: Bot) -> None:
    await query.message.delete()
    row = """'<a href=\"tg://user?id={user_id}\">{user_name}</a>' : <code>{user_id}</code> - {ref_count}\n"""
    result = ""
    s = get_session()
    if callback_data.duration is None:
        header = "Лучшие рефоводы за всё время\n"
        result += header
        for u in await get_tg_users_by_id(get_top_users_by_referrals(s, 25), bot):
            result += row.format(user_id=u[0], user_name=u[2].username, ref_count=u[1])
    else:
        start_date = datetime.now() - timedelta(seconds=callback_data.duration)
        header = f"Лучшие рефоводы c {start_date}\n"
        result += header
        for u in await get_tg_users_by_id(get_top_users_by_referrals_with_start_date(s, start_date, 25), bot):
            result += row.format(user_id=u[0], user_name=u[2].username, ref_count=u[1])
    await query.message.answer(text=result)


async def get_tg_users_by_id(users, bot: Bot) -> list[list]:
    result = []
    for row in users:
        result.append([row[0], row[1], await bot.get_chat(row[0])])
    return result


@router.callback_query(ChangeRefPay.filter(), UserExistsFilter())
async def ref_pay_change_handler(query: CallbackQuery, lang: Lang, state: FSMContext) -> None:
    await query.message.delete()
    await state.set_state(SettingsStates.change_ref_pay)
    await query.message.answer(text=format_string(get_message(MessageKey.ADMIN_CHANGE_REF_PAY, lang),
                                                  pay_for_ref=await get_setting(SettingsKey.PAY_FOR_REFERRAL)),
                               reply_markup=with_exit_button(lang))


@router.message(SettingsStates.change_ref_pay, UserExistsFilter())
async def process_ref_pay_change(message: Message, lang: Lang, state: FSMContext) -> None:
    try:
        value = int(message.text)
        if value >= 0:
            await update_setting(SettingsKey.PAY_FOR_REFERRAL, value)
            await state.clear()
            await message.answer(format_string(get_message(MessageKey.ADMIN_CHANGE_REF_PAY_SUCCESSFULLY, lang),
                                               pay_for_ref=await get_setting(SettingsKey.PAY_FOR_REFERRAL)))
        else:
            await message.reply("Number out of bounds.")
    except ValueError:
        await message.reply("Please enter a valid integer.")
