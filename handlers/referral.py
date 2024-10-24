import logging
import os

from aiogram import Bot, Router
from aiogram.types import CallbackQuery, FSInputFile
from mako.exceptions import RuntimeException
from sqlalchemy.ext.asyncio import AsyncSession

import settings
import transaction_manager
from database import get_user_by_tg, User, is_good_user_by_tg, TransactionOperation, SettingsKey, \
    get_user_referrals_count, with_session
from filters.base_filters import UserExistsFilter
from keyboard_markup.inline_user_kb import get_user_share_ref_link_kbm
from lang.lang_based_provider import Lang, get_message, MessageKey, format_string
from lang.lang_provider import get_cached_lang
from lang_based_variable import MenuToRefCallback
from providers.tg_arg_provider import TgArg, ArgType
from settings import get_setting
from variables import bot

router = Router(name="referral_router")

logger = logging.getLogger(__name__)


@with_session
async def process_paying_for_referral(user_id: int, s: AsyncSession) -> None:
    try:
        user: User = await get_user_by_tg(user_id, s=s)
        if user.referred_by_id is None:
            return
        if await is_good_user_by_tg(user.referred_by_id, s=s, cache_id=user.referred_by_id):
            ref_pay_amount = await settings.get_setting(SettingsKey.PAY_FOR_REFERRAL)
            await transaction_manager.make_transaction_from_system(target=user.referred_by_id,
                                                                   created_by=user.telegram_id,
                                                                   operation=TransactionOperation.INCREMENT,
                                                                   amount=ref_pay_amount,
                                                                   description="Payment for referral",
                                                                   session=s)
            await bot.send_message(chat_id=user.referred_by_id,
                                   text=format_string(get_message(MessageKey.REF_INVITED_STEP_TWO, await get_cached_lang(user.referred_by_id)),
                                                      user_link=user_id, amount=ref_pay_amount))
        else:
            user.referred_by_id = None
    except RuntimeException as e:
        logger.error('failed pay for referral', e)


@router.callback_query(MenuToRefCallback.filter(), UserExistsFilter())
async def process_menu_to_ref_callback(query: CallbackQuery, lang: Lang, bot: Bot) -> None:
    await query.message.delete()
    ref_link = TgArg(query.from_user.id).encode(ArgType.REFERRAL)
    await bot.send_photo(chat_id=query.message.chat.id,
                         photo=FSInputFile(path=os.getenv("PHOTO_01_PATH")),
                         caption=format_string(get_message(MessageKey.REF_INVITE, lang),
                                               ref_invite_pay=await get_setting(SettingsKey.PAY_FOR_REFERRAL),
                                               link=ref_link,
                                               ref_invite_count=await get_user_referrals_count(query.from_user.id, cache_id=query.from_user.id)),
                         reply_markup=get_user_share_ref_link_kbm(lang, [("ref_link", ref_link)]))
