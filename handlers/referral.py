import os

from aiogram import Bot, Router
from aiogram.types import Message, CallbackQuery, FSInputFile

import settings
import transaction_manager
from database import get_user_by_tg, User, get_session, is_good_user_by_tg, TransactionOperation, SettingsKey, \
    get_user_referrals_count
from filters.base_filters import UserExistsFilter
from keyboard_markup.inline_user_kb import get_user_share_ref_link_kbm
from lang.lang_based_provider import Lang, get_message, MessageKey, format_string
from lang.lang_provider import get_cached_lang
from lang_based_variable import MenuToRefCallback
from providers.tg_arg_provider import TgArg, ArgType
from settings import get_setting

router = Router(name="referral_router")


async def process_paying_for_referral(user_id: int, bot: Bot) -> None:
    session = get_session()
    user: User = get_user_by_tg(session, user_id)
    if user.referred_by_id is None:
        return
    if await is_good_user_by_tg(session, user.referred_by_id):
        ref_pay_amount = await settings.get_setting(SettingsKey.PAY_FOR_REFERRAL)
        transaction_manager.make_transaction_from_system(target=user.referred_by_id,
                                                         created_by=user.telegram_id,
                                                         operation=TransactionOperation.INCREMENT,
                                                         amount=ref_pay_amount,
                                                         description="Payment for referral")
        await bot.send_message(chat_id=user.referred_by_id,
                               text=format_string(get_message(MessageKey.REF_INVITED_STEP_TWO, await get_cached_lang(user.referred_by_id)),
                                                  user_link=user_id, amount=ref_pay_amount))
    else:
        user.referred_by_id = None
        session.commit()


def build_ref_link(message: Message) -> str:
    arg = TgArg(ArgType.REFERRAL, message.from_user.id)
    return arg.get()


@router.callback_query(MenuToRefCallback.filter(), UserExistsFilter())
async def process_menu_to_ref_callback(query: CallbackQuery, lang: Lang, bot: Bot) -> None:
    ref_link = TgArg.of(ArgType.REFERRAL, query.from_user.id)
    await bot.send_photo(chat_id=query.message.chat.id,
                         photo=FSInputFile(path=os.getenv("PHOTO_01_PATH")),
                         caption=format_string(get_message(MessageKey.REF_INVITE, lang),
                                               ref_invite_pay=await get_setting(SettingsKey.PAY_FOR_REFERRAL),
                                               link=ref_link,
                                               ref_invite_count=await get_user_referrals_count(get_session(), query.from_user.id, cache_id=query.from_user.id)),
                         reply_markup=get_user_share_ref_link_kbm(lang, [("ref_link", ref_link)]))
