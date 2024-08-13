from datetime import timedelta

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from lang.lang_based_provider import *
from lang_based_variable import Lang, KeyboardKey, LangSetCallback

TEXT = "text"
REF = "ref"


def get_builder(markup=None):
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


def build_markup(lang: Lang, k: KeyboardKey,
                 source_markup: InlineKeyboardMarkup = None,
                 url_params: list = None,
                 callback_data_param: list = None) -> InlineKeyboardMarkup:
    if url_params is None:
        url_params = []
    if callback_data_param is None:
        callback_data_param = []
    if source_markup is not None:
        source_markup = source_markup.inline_keyboard
    builder = get_builder(markup=source_markup)
    url_params_p = 0
    callback_data_param_p = 0
    for row in get_keyboard(k, lang):
        kbs: list["InlineKeyboardButton"] = []
        for m in row:
            if m.with_url_placeholder:
                kbs.append(build_inline_keyboard_button(m, url_params[url_params_p], kbk=k, lang=lang))
                url_params_p += 1
            elif m.with_callback_param_required:
                kbs.append(build_inline_keyboard_button(m, **callback_data_param[callback_data_param_p]))
                callback_data_param_p += 1
            else:
                kbs.append(build_inline_keyboard_button(m, kbk=k, lang=lang))
        builder.row(*kbs)
    return builder.as_markup()


def get_lang_kbm() -> InlineKeyboardMarkup:
    builder = get_builder()
    for lang in Lang:
        builder.button(text=lang.value, callback_data=LangSetCallback(lang=lang).pack())
    return builder.as_markup()


def get_require_subscription_kbm(lang: Lang) -> InlineKeyboardMarkup:
    return build_markup(lang, KeyboardKey.START_REQUIRE_SUBSCRIPTION_KB)


def get_user_menu_kbm(lang: Lang) -> InlineKeyboardMarkup:
    return build_markup(lang, KeyboardKey.INLINE_MENU)


def get_user_share_ref_link_kbm(lang: Lang, params: list) -> InlineKeyboardMarkup:
    return build_markup(lang, KeyboardKey.REF_LINK_SHARE, url_params=params)


def get_profile_kbm(lang: Lang) -> InlineKeyboardMarkup:
    return build_markup(lang, KeyboardKey.PROFILE)


def with_exit_button(lang: Lang, markup: InlineKeyboardMarkup | None = None) -> InlineKeyboardMarkup:
    return build_markup(lang, KeyboardKey.EXIT, source_markup=markup)


def with_step_back_button(lang: Lang, markup: InlineKeyboardMarkup | None = None) -> InlineKeyboardMarkup:
    return build_markup(lang, KeyboardKey.STEP_BACK, source_markup=markup)


def get_buy_premium_menu_kbm(lang: Lang) -> InlineKeyboardMarkup:
    return build_markup(lang, KeyboardKey.BUY_PREMIUM_MENU)


def get_admin_menu_kbm(lang: Lang) -> InlineKeyboardMarkup:
    return build_markup(lang, KeyboardKey.ADMIN_PANEL, callback_data_param=[{"duration": None}, {"duration": timedelta(weeks=1).total_seconds()}])


def get_yes_no_kbm(lang: Lang) -> InlineKeyboardMarkup:
    return build_markup(lang, KeyboardKey.YES_NO)


def get_mailing_add_button_or_preview_kbm(lang: Lang) -> InlineKeyboardMarkup:
    return build_markup(lang, KeyboardKey.ADMIN_MAILING_ADD_BUTTON_OR_PREVIEW)


def get_mailing_inline_button_preview_kbm(lang: Lang, markup: InlineKeyboardMarkup | None = None) -> InlineKeyboardMarkup:
    return build_markup(lang, KeyboardKey.ADMIN_MAILING_INLINE_BUTTON_PREVIEW, source_markup=markup)


def get_mailing_start_kbm(lang: Lang) -> InlineKeyboardMarkup:
    return build_markup(lang, KeyboardKey.ADMIN_MAILING_START)


def get_mailing_menu_kbm(lang: Lang, params: list[dict]) -> InlineKeyboardMarkup:
    return build_markup(lang, KeyboardKey.ADMIN_MAILING_MENU, callback_data_param=params)


def get_mailing_queue_fill_retry_kbm(lang: Lang, params: list[dict]) -> InlineKeyboardMarkup:
    return build_markup(lang, KeyboardKey.ADMIN_MAILING_QUEUE_FILL_RETRY, callback_data_param=params)
