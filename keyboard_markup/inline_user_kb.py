from datetime import timedelta

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from lang.lang_based_provider import *
from lang_based_variable import Lang, KeyboardKey, LangSetCallback

TEXT = "text"
REF = "ref"


def __get_builder(markup=None):
    return InlineKeyboardBuilder(markup=markup)


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


def build_markup(lng: Lang, k: KeyboardKey,
                 source_markup: InlineKeyboardMarkup = None,
                 url_params: list = None,
                 callback_data_param: list = None) -> InlineKeyboardMarkup:
    if url_params is None:
        url_params = []
    if callback_data_param is None:
        callback_data_param = []
    if source_markup is not None:
        source_markup = source_markup.inline_keyboard
    builder = __get_builder(markup=source_markup)
    url_params_p = 0
    callback_data_param_p = 0
    for row in get_keyboard(k, lng):
        kbs: list["InlineKeyboardButton"] = []
        for m in row:
            if m.with_url_placeholder:
                kbs.append(build_inline_keyboard_button(m, url_params[url_params_p], kbk=k, lang=lng))
                url_params_p += 1
            elif m.with_callback_param_required:
                kbs.append(build_inline_keyboard_button(m, **callback_data_param[callback_data_param_p]))
                callback_data_param_p += 1
            else:
                kbs.append(build_inline_keyboard_button(m, kbk=k, lang=lng))
        builder.row(*kbs)
    return builder.as_markup()


def get_lang_kbm() -> InlineKeyboardMarkup:
    builder = __get_builder()
    for lang in Lang:
        builder.button(text=lang.value, callback_data=LangSetCallback(lang=lang).pack())
    return builder.as_markup()


def get_require_subscription_kbm(lng: Lang) -> InlineKeyboardMarkup:
    return build_markup(lng, KeyboardKey.START_REQUIRE_SUBSCRIPTION_KB)


def get_user_menu_kbm(lng: Lang) -> InlineKeyboardMarkup:
    return build_markup(lng, KeyboardKey.INLINE_MENU)


def get_user_share_ref_link_kbm(lng: Lang, params: list) -> InlineKeyboardMarkup:
    return build_markup(lng, KeyboardKey.REF_LINK_SHARE, url_params=params)


def get_profile_kbm(lng: Lang) -> InlineKeyboardMarkup:
    return build_markup(lng, KeyboardKey.PROFILE)


def with_exit_button(lng: Lang, markup: InlineKeyboardMarkup | None = None) -> InlineKeyboardMarkup:
    return build_markup(lng, KeyboardKey.EXIT, source_markup=markup)


def get_buy_premium_menu_kbm(lng: Lang) -> InlineKeyboardMarkup:
    return build_markup(lng, KeyboardKey.BUY_PREMIUM_MENU)


def get_admin_menu_kbm(lng: Lang) -> InlineKeyboardMarkup:
    return build_markup(lng, KeyboardKey.ADMIN_PANEL, callback_data_param=[{"duration": None}, {"duration": timedelta(weeks=1).total_seconds()}])
