from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from lang.lang_based_provider import *
from lang_based_variable import Lang, KeyboardKey, LangSetCallback

TEXT = "text"
REF = "ref"


def __get_builder():
    return InlineKeyboardBuilder()


def build_inline_keyboard_button(m: M, **kwargs) -> InlineKeyboardButton:
    if not m.__dict__.__contains__('callback_class'):
        return InlineKeyboardButton(text=m.text,
                                    url=m.url)
    else:
        return InlineKeyboardButton(text=m.text,
                                    callback_data=m.get_callback_instance(**kwargs).pack())


def build_markup(lng: Lang, k: KeyboardKey) -> InlineKeyboardMarkup:
    builder = __get_builder()
    for row in get_keyboard(k, lng):
        kbs: list["InlineKeyboardButton"] = []
        for m in row:
            kbs.append(build_inline_keyboard_button(m, kbk=k, lang=lng))
        builder.row(*kbs)
    return builder.as_markup()


def get_start_user_kbm() -> InlineKeyboardMarkup:
    builder = __get_builder()
    for lang in Lang:
        builder.button(text=lang.value, callback_data=LangSetCallback(lang=lang).pack())
    return builder.as_markup()


def get_require_subscription_kbm(lng: Lang) -> InlineKeyboardMarkup:
    return build_markup(lng, KeyboardKey.START_REQUIRE_SUBSCRIPTION_KB)


def get_user_menu_kbm(lng: Lang) -> InlineKeyboardMarkup:
    return build_markup(lng, KeyboardKey.INLINE_MENU)
