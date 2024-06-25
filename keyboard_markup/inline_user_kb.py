from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from callbacks.start import CheckStartMembershipCallback, LangSetCallback
from lang.lang_based_text_provider import *


def __get_builder():
    return InlineKeyboardBuilder()


def get_start_user_kbm() -> InlineKeyboardMarkup:
    builder = __get_builder()
    for lang in Lang:
        builder.button(text=lang.value, callback_data=LangSetCallback(lang=lang).pack())
    return builder.as_markup()


def get_require_subscription_kbm(lng: Lang) -> InlineKeyboardMarkup:
    builder = __get_builder()
    kbs = get_keyboard(KeyboardKey.START_REQUIRE_SUBSCRIPTION_KB, lng)
    builder.row(
        InlineKeyboardButton(text=kbs.get(1).get('text'), url=kbs.get(1).get('ref')),
        InlineKeyboardButton(text=kbs.get(2).get('text'), url=kbs.get(2).get('ref'))
    )
    builder.row(
        InlineKeyboardButton(text=kbs.get(3).get('text'), url=kbs.get(3).get('ref'))
    )
    builder.row(
        InlineKeyboardButton(
            text=kbs.get(4).get('text'),
            callback_data=CheckStartMembershipCallback(kbk=KeyboardKey.START_REQUIRE_SUBSCRIPTION_KB, lang=lng).pack()))
    return builder.as_markup()
