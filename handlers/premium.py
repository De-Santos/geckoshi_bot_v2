import os

from aiogram import Router, Bot
from aiogram.types import CallbackQuery, FSInputFile

import transaction_manager
from database import get_user_by_tg, SettingsKey, TransactionOperation, update_user_premium
from filters.base_filters import UserExistsFilter
from keyboard_markup.inline_user_kb import get_buy_premium_menu_kbm
from lang.lang_based_provider import get_message, format_string
from lang_based_variable import BuyPremium, Lang, MessageKey, BuyPremiumMenu
from middleware.metadata_providers import IsPremiumUserMiddleware
from settings import get_setting

router = Router(name="premium_router")

router.callback_query.middleware(IsPremiumUserMiddleware())


@router.callback_query(BuyPremiumMenu.filter(), UserExistsFilter())
async def buy_premium_menu(query: CallbackQuery, is_premium: bool, lang: Lang, bot: Bot) -> None:
    if is_premium:
        await query.answer(get_message(MessageKey.PREMIUM_ALREADY_BOUGHT, lang), show_alert=True)
        return
    await query.message.delete()
    await bot.send_photo(chat_id=query.message.chat.id,
                         photo=FSInputFile(path=os.getenv("PHOTO_01_PATH")),
                         caption=format_string(get_message(MessageKey.PREMIUM_BUY_MENU, lang), premium_gmeme_price=await get_setting(SettingsKey.PREMIUM_GMEME_PRICE)),
                         reply_markup=get_buy_premium_menu_kbm(lang))


@router.callback_query(BuyPremium.filter(), UserExistsFilter())
async def buy_premium_callback_handler(query: CallbackQuery, is_premium: bool, lang: Lang) -> None:
    if is_premium:
        await query.answer(get_message(MessageKey.PREMIUM_ALREADY_BOUGHT, lang), show_alert=True)
        return
    user = await get_user_by_tg(query.from_user.id)
    gmeme_price = await get_setting(SettingsKey.PREMIUM_GMEME_PRICE)
    if user.balance - gmeme_price < 0:
        await query.answer(format_string(get_message(MessageKey.NOT_ENOUGH_TO_BUY_PREMIUM, lang), not_enough=gmeme_price - user.balance), show_alert=True)
    else:
        await transaction_manager.make_transaction_from_system(target=user.telegram_id,
                                                               created_by=user.telegram_id,
                                                               operation=TransactionOperation.DECREMENT,
                                                               amount=gmeme_price,
                                                               description="Buy premium")
        await update_user_premium(user.telegram_id, True)
        await query.message.answer(get_message(MessageKey.PREMIUM_HAS_BOUGHT, lang))
