from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from lang.lang_based_provider import *
from lang_based_variable import Lang, KeyboardKey, LangSetCallback

TEXT = "text"
REF = "ref"


def __get_builder():
    return InlineKeyboardBuilder()


def build_inline_keyboard_button(m: M, url_param=None, **kwargs) -> InlineKeyboardButton:
    if url_param is not None and m.callback_class is None:
        return InlineKeyboardButton(text=m.text,
                                    url=format_string(m.url, **dict([url_param])))
    elif m.callback_class is None:
        return InlineKeyboardButton(text=m.text,
                                    url=m.url)
    else:
        return InlineKeyboardButton(text=m.text,
                                    callback_data=m.get_callback_instance(**kwargs).pack())


def build_markup(lng: Lang, k: KeyboardKey, url_params: list = None) -> InlineKeyboardMarkup:
    if url_params is None:
        url_params = []
    builder = __get_builder()
    url_params_p = 0
    for row in get_keyboard(k, lng):
        kbs: list["InlineKeyboardButton"] = []
        for m in row:
            if m.with_url_placeholder:
                kbs.append(build_inline_keyboard_button(m, url_params[url_params_p], kbk=k, lang=lng))
                url_params_p += 1
            else:
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


def get_user_share_ref_link_kbm(lng: Lang, params: list) -> InlineKeyboardMarkup:
    return build_markup(lng, KeyboardKey.REF_LINK_SHARE, params)
