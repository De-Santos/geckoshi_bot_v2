import os

from aiogram import Bot, Router
from aiogram.types import CallbackQuery, FSInputFile

from database import SettingsKey, get_user_referrals_count, get_session, User, get_user_by_tg, TransactionType
from filters.base_filters import UserExistsFilter
from keyboard_markup.inline_user_kb import get_profile_kbm
from lang.lang_based_provider import Lang, format_string, get_message
from lang_based_variable import MenuToProfileCallback, MessageKey, ProfileWithdraw
from settings import get_setting
from transaction_manager.manager import select_transactions_sum_amount

router = Router(name="profile_router")


@router.callback_query(MenuToProfileCallback.filter(), UserExistsFilter())
async def process_profile_callback(query: CallbackQuery, lang: Lang, bot: Bot) -> None:
    s = get_session()
    user: User = get_user_by_tg(s, query.from_user.id)
    await query.message.delete()
    await bot.send_photo(chat_id=query.message.chat.id,
                         photo=FSInputFile(path=os.getenv("PHOTO_01_PATH")),
                         caption=format_string(
                             get_message(MessageKey.USER_PROFILE, lang),
                             user_link=user.telegram_id,
                             user_name=query.from_user.first_name,
                             user_tg_id=user.telegram_id,
                             is_premium_account=user.is_premium,
                             balance=user.balance,
                             ref_count=await get_user_referrals_count(s, user.telegram_id, cache_id=user.telegram_id),
                             withdrew=select_transactions_sum_amount(user.telegram_id, TransactionType.WITHDRAW),
                             min_withdraw_in_airdrop=await get_setting(SettingsKey.MIN_WITHDRAW_IN_AIRDROP)),
                         reply_markup=get_profile_kbm(lang))


@router.callback_query(ProfileWithdraw.filter(), UserExistsFilter())
async def process_profile_callback(query: CallbackQuery, lang: Lang) -> None:
    await query.answer(text=get_message(MessageKey.FUNCTION_NOT_IMPLEMENTED, lang))
