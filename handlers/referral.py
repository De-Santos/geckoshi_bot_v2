from aiogram import Bot
from aiogram.types import Message

import settings
import transaction_manager
from database import get_user_by_tg, User, get_session, is_good_user_by_tg, TransactionOperation, SettingsKey
from lang.lang_based_text_provider import Lang, get_message, MessageKey
from lang.lang_provider import get_cached_lang


async def process_paying_for_referral(message: Message, bot: Bot, lang: Lang) -> None:
    session = get_session()
    user: User = get_user_by_tg(session, message.from_user.id)
    if user.referred_by_id is not None and is_good_user_by_tg(session, user.referred_by_id):
        ref_pay_amount = settings.get_setting(session, SettingsKey.PAY_FOR_REFERRAL)
        transaction_manager.make_transaction(tg_user_id=user.telegram_id, created_by=user.referred_by_id,
                                             operation=TransactionOperation.INCREMENT,
                                             amount=ref_pay_amount,
                                             description="Payment for referral")
        await bot.send_message(chat_id=user.referred_by_id,
                               text=get_message(MessageKey.REF_INVITED_STEP_TWO,
                                                await get_cached_lang(user.referred_by_id)).format(
                                   user_link=message.from_user.id, amount=ref_pay_amount))
