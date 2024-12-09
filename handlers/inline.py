import logging
from uuid import uuid4

from aiogram import Router
from aiogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent
from fastapi import HTTPException

import links
from api.cheque_api.activation.impl import get_cheque_impl
from api.cheque_api.dto import ChequeDto
from database import CurrencyType
from exceptions.cheque import ChequeInactive, ChequeForbidden
from filters.base_filters import UserExistsFilter
from keyboard_markup.inline_user_kb import get_inline_mode_share_ref_link_button_kbm, get_inline_mode_cheque_activate_button
from lang.lang_based_provider import get_message, format_string
from lang_based_variable import Lang, MessageKey
from providers.tg_arg_provider import TgArg, ArgType

router = Router(name="inline_router")
logger = logging.getLogger(__name__)


@router.inline_query(UserExistsFilter())
async def inline_echo(query: InlineQuery, lang: Lang) -> None:
    arg = TgArg(query.query.strip())
    if not arg.parse():
        await query.answer(results=generate_default_result(query, lang), cache_time=1)
        return

    if arg.get_type() == ArgType.CHEQUE:
        await answer_cheque_result(query, lang, arg.get())
        return


async def answer_cheque_result(query: InlineQuery, lang: Lang, cheque_id: int) -> None:
    try:
        cheque: ChequeDto = await get_cheque_impl(cheque_id, query.from_user.id)
    except HTTPException as e:
        logger.warning("Failed to retrieve cheque data. User ID: %s, Cheque ID: %s, Exception: %s", query.from_user.id, cheque_id, str(e), exc_info=e)
        await query.answer([], cache_time=1, switch_pm_text=exception_translater(e, lang))
        return

    cheque_result = InlineQueryResultArticle(
        id=str(uuid4()),
        title=cheque.name + " " + f"{cheque.amount_per_user:.2f}" + f" {CurrencyType(cheque.currency_type).name}",
        description=cheque.description,
        input_message_content=InputTextMessageContent(message_text=get_cheque_message(cheque)),
        reply_markup=get_inline_mode_cheque_activate_button(links.generate(ArgType.CHEQUE, cheque.id))
    )
    await query.answer([cheque_result], cache_time=1)


def generate_default_result(query: InlineQuery, lang: Lang) -> list[InlineQueryResultArticle]:
    invite_link_result = InlineQueryResultArticle(
        id=str(uuid4()),
        title=get_message(MessageKey.INLINE_MODE_SHARE_REF_LINK_INLINE_TITLE, lang),
        description=get_message(MessageKey.INLINE_MODE_SHARE_REF_LINK_INLINE_DESCRIPTION, lang),
        input_message_content=InputTextMessageContent(message_text=get_message(MessageKey.INLINE_MODE_SHARE_REF_LINK_MESSAGE)),
        reply_markup=get_inline_mode_share_ref_link_button_kbm(links.generate(ArgType.REFERRAL, query.from_user.id))
    )
    return [invite_link_result]


def exception_translater(e: Exception, lang: Lang) -> str | None:
    if isinstance(e, ChequeInactive):
        return get_message(MessageKey.CHEQUE_INACTIVE, lang)
    if isinstance(e, ChequeForbidden):
        return get_message(MessageKey.CHEQUE_FORBIDDEN, lang)

    return None


def get_cheque_message(cheque: ChequeDto) -> str:
    return format_string(get_message(MessageKey.INLINE_MODE_CHEQUE_MESSAGE),
                         amount=cheque.amount_per_user,
                         currency='$' + CurrencyType(cheque.currency_type).name)
