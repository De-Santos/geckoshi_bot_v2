from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from callbacks.start import CheckStartMembershipCallback, LangSetCallback
from lang.lang_based_text_provider import *
from callbacks.user_menu import *

TEXT = "text"
REF = "ref"


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
        InlineKeyboardButton(text=kbs.get(1).get(TEXT), url=kbs.get(1).get(REF)),
        InlineKeyboardButton(text=kbs.get(2).get(TEXT), url=kbs.get(2).get(REF))
    )
    builder.row(
        InlineKeyboardButton(text=kbs.get(3).get(TEXT), url=kbs.get(3).get(REF))
    )
    builder.row(
        InlineKeyboardButton(
            text=kbs.get(4).get(TEXT),
            callback_data=CheckStartMembershipCallback(kbk=KeyboardKey.START_REQUIRE_SUBSCRIPTION_KB, lang=lng).pack()))
    return builder.as_markup()


def get_user_menu_kbm(lng: Lang) -> InlineKeyboardMarkup:
    builder = __get_builder()
    kbs = get_keyboard(KeyboardKey.INLINE_MENU, lng)
    row = 1
    builder.row(
        InlineKeyboardButton(text=kbs.get(row).get(1).get(TEXT), callback_data=MenuToRefCallback().pack()),
        InlineKeyboardButton(text=kbs.get(row).get(2).get(TEXT), callback_data=MenuToBonusCallback().pack())
    )
    row += 1
    builder.row(
        InlineKeyboardButton(text=kbs.get(row).get(1).get(TEXT), callback_data=MenuToTasksCallback().pack()),
        InlineKeyboardButton(text=kbs.get(row).get(2).get(TEXT), callback_data=MenuToChequeCallback().pack())
    )
    row += 1
    builder.row(
        InlineKeyboardButton(text=kbs.get(row).get(1).get(TEXT), callback_data=MenuToP2PCallback().pack()),
        InlineKeyboardButton(text=kbs.get(row).get(2).get(TEXT), callback_data=MenuToSlotsCallback().pack())
    )
    row += 1
    builder.row(
        InlineKeyboardButton(text=kbs.get(row).get(1).get(TEXT), callback_data=MenuToNFTCallback().pack()),
        InlineKeyboardButton(text=kbs.get(row).get(2).get(TEXT), callback_data=MenuToProfileCallback().pack())
    )
    row += 1
    builder.row(
        InlineKeyboardButton(text=kbs.get(row).get(1).get(TEXT), callback_data=MenuToStatistic().pack()),
    )
    return builder.as_markup()
