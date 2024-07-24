from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from lang.lang_based_provider import Lang, get_keyboard, KeyboardKey
from lang_based_variable import M


def __get_builder():
    return ReplyKeyboardBuilder()


def build_keyboard_button(m: M) -> KeyboardButton:
    return KeyboardButton(text=m.text)


def build_markup(builder: ReplyKeyboardBuilder, lng: Lang, k: KeyboardKey) -> ReplyKeyboardBuilder:
    for row in get_keyboard(k, lng):
        kbs: list["KeyboardButton"] = []
        for m in row:
            kbs.append(build_keyboard_button(m))
        builder.row(*kbs)
    return builder


def get_reply_keyboard_kbm(lng: Lang, is_admin: bool = False) -> ReplyKeyboardMarkup:
    builder = __get_builder()
    build_markup(builder, lng, KeyboardKey.MENU)
    if is_admin:
        build_markup(builder, lng, KeyboardKey.ADMIN_MENU)
    return builder.as_markup(resize_keyboard=True)
