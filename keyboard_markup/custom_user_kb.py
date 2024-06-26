from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from lang.lang_based_text_provider import Lang, get_keyboard, KeyboardKey


def __get_builder():
    return ReplyKeyboardBuilder()


def get_reply_keyboard_kbm(lng: Lang, is_admin: bool = False) -> ReplyKeyboardMarkup:
    builder = __get_builder()
    kbs = get_keyboard(KeyboardKey.MENU, lng)
    builder.row(KeyboardButton(text=kbs.get('text')))
    if is_admin:
        a_kbs = get_keyboard(KeyboardKey.ADMIN_MENU, lng)
        builder.row(KeyboardButton(text=a_kbs.get('text')))
    return builder.as_markup(resize_keyboard=True)
