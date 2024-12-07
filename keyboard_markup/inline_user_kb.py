from datetime import timedelta
from typing import Optional, List, Union

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database import TaskType
from database.enums import ChequeType
from lang.lang_based_provider import *
from lang_based_variable import Lang, KeyboardKey, LangSetCallback

TEXT = "text"
REF = "ref"


def get_builder(markup=None):
    return InlineKeyboardBuilder(markup=markup)


def build_inline_keyboard_button(m: M, text_param=None, url_param=None, **kwargs) -> InlineKeyboardButton:
    text = m.text
    if m.with_text_param_required:
        text = format_string(m.text, **text_param)
    if url_param is not None and m.callback_class is None:
        return InlineKeyboardButton(text=text,
                                    url=format_string(m.url, **url_param))
    elif m.callback_class is None:
        return InlineKeyboardButton(text=text,
                                    url=m.url)
    else:
        return InlineKeyboardButton(text=text,
                                    callback_data=m.get_callback_instance(**kwargs).pack())


def build_markup(lang: Lang | None, k: KeyboardKey,
                 source_markup: InlineKeyboardMarkup = None,
                 url_params: Optional[List[Union[str, dict]]] = None,
                 callback_data_param: Optional[List[dict]] = None,
                 text_params: Optional[List[dict]] = None) -> InlineKeyboardMarkup:
    if url_params is None:
        url_params = []
    if callback_data_param is None:
        callback_data_param = []
    if text_params is None:
        text_params = []
    if source_markup is not None:
        source_markup = source_markup.inline_keyboard
    builder = get_builder(markup=source_markup)
    url_params_p = 0
    callback_data_param_p = 0
    text_params_p = 0

    for row in get_keyboard(k, lang):
        kbs: list[InlineKeyboardButton] = []
        for m in row:
            url_param = None
            text_param = None
            if m.with_url_placeholder:
                url_param = url_params[url_params_p]
                url_params_p += 1
            if m.with_text_param_required:
                text_param = text_params[text_params_p]
                text_params_p += 1

            if m.with_callback_param_required:
                kbs.append(build_inline_keyboard_button(m, url_param=url_param, text_param=text_param, **callback_data_param[callback_data_param_p]))
                callback_data_param_p += 1
            else:
                kbs.append(build_inline_keyboard_button(m, url_param=url_param, text_param=text_param, kbk=k, lang=lang))

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


def with_skip_button(lang: Lang, markup: InlineKeyboardMarkup | None = None) -> InlineKeyboardMarkup:
    return build_markup(lang, KeyboardKey.SKIP, source_markup=markup)


def with_step_back_button(lang: Lang, markup: InlineKeyboardMarkup | None = None) -> InlineKeyboardMarkup:
    return build_markup(lang, KeyboardKey.STEP_BACK, source_markup=markup)


def get_buy_premium_menu_kbm(lang: Lang) -> InlineKeyboardMarkup:
    return build_markup(lang, KeyboardKey.BUY_PREMIUM_MENU)


def get_admin_menu_kbm(lang: Lang) -> InlineKeyboardMarkup:
    return build_markup(lang, KeyboardKey.ADMIN_PANEL, callback_data_param=[{"duration": None}, {"duration": timedelta(weeks=1).total_seconds()}])


def get_yes_no_kbm(lang: Lang) -> InlineKeyboardMarkup:
    return build_markup(lang, KeyboardKey.YES_NO)


def get_add_button_or_preview_kbm(lang: Lang) -> InlineKeyboardMarkup:
    return build_markup(lang, KeyboardKey.ADMIN_ADD_BUTTON_OR_PREVIEW)


def get_inline_button_preview_kbm(lang: Lang, markup: InlineKeyboardMarkup | None = None) -> InlineKeyboardMarkup:
    return build_markup(lang, KeyboardKey.ADMIN_INLINE_BUTTON_PREVIEW, source_markup=markup)


def get_mailing_start_kbm(lang: Lang) -> InlineKeyboardMarkup:
    return build_markup(lang, KeyboardKey.ADMIN_MAILING_START)


def get_mailing_menu_kbm(lang: Lang, params: list[dict]) -> InlineKeyboardMarkup:
    return build_markup(lang, KeyboardKey.ADMIN_MAILING_MENU, callback_data_param=params)


def get_mailing_queue_fill_retry_kbm(lang: Lang, params: list[dict]) -> InlineKeyboardMarkup:
    return build_markup(lang, KeyboardKey.ADMIN_MAILING_QUEUE_FILL_RETRY, callback_data_param=params)


def get_slots_menu_kbm(lang: Lang) -> InlineKeyboardMarkup:
    params = [
        {'amount': 100},
        {'amount': 250},
        {'amount': 500},
        {'amount': 1000},
        {'amount': 2500},
        {'amount': 5000},
        {'amount': 10000},
    ]
    return with_back_to_menu_button(lang, build_markup(None, KeyboardKey.SLOTS_MENU, text_params=params, callback_data_param=params))


def get_slots_continue_kbm(lang: Lang, params: list[dict]) -> InlineKeyboardMarkup:
    return build_markup(lang, KeyboardKey.SLOTS_CONTINUE_PLAY, callback_data_param=params)


def with_back_to_menu_button(lang: Lang, source_markup: InlineKeyboardMarkup = None, remove_source: bool = False) -> InlineKeyboardMarkup:
    return build_markup(lang, KeyboardKey.BACK_TO_MENU, source_markup=source_markup, callback_data_param=[{'remove_source': remove_source}])


def get_task_menu_kbm(lang: Lang) -> InlineKeyboardMarkup:
    return build_markup(lang, KeyboardKey.TASK_MENU)


def get_admin_task_type_menu_kbm() -> InlineKeyboardMarkup:
    params = [{'task_type': i} for i in TaskType]
    return build_markup(None, KeyboardKey.ADMIN_TASK_TYPE_MENU, callback_data_param=params)


def get_add_more_buttons_or_continue_kbm(lang: Lang) -> InlineKeyboardMarkup:
    return build_markup(lang, KeyboardKey.ADMIN_ADD_MORE_BUTTONS_OR_CONTINUE)


def get_continue_or_retry_kbm(lang: Lang) -> InlineKeyboardMarkup:
    return build_markup(lang, KeyboardKey.CONTINUE_OR_RETRY)


def get_save_kbm(lang: Lang, source_markup: InlineKeyboardMarkup = None) -> InlineKeyboardMarkup:
    return build_markup(lang, KeyboardKey.SAVE, source_markup=source_markup)


def get_delete_task_menu_kbm(lang: Lang, task_id: int) -> InlineKeyboardMarkup:
    return build_markup(lang, KeyboardKey.DELETE_TASK_MENU, callback_data_param=[{'task_id': task_id}])


def get_task_type_menu_kbm(lang: Lang) -> InlineKeyboardMarkup:
    params = [
        {
            'task_type': TaskType.TIME_BASED.value,
            'page': 1
        },
        {
            'task_type': TaskType.DONE_BASED.value,
            'page': 1
        },
        {
            'task_type': TaskType.POOL_BASED.value,
            'page': 1
        },
    ]
    return with_back_to_menu_button(lang, build_markup(None, KeyboardKey.TASK_TYPE_MENU, callback_data_param=params))


def get_select_task_nav_menu_kbm(lang: Lang, done_params: list[dict], params: list[dict], source_markup: InlineKeyboardMarkup = None) -> InlineKeyboardMarkup:
    return with_task_navigation_menu(lang, params, with_task_submit_button(lang, done_params, source_markup))


def with_task_submit_button(lang: Lang, params: list[dict], source_markup: InlineKeyboardMarkup = None) -> InlineKeyboardMarkup:
    return build_markup(lang, KeyboardKey.SELECT_TASK_SUBMIT_BUTTON, callback_data_param=params, source_markup=source_markup)


def with_task_navigation_menu(lang: Lang, params: list[dict], source_markup: InlineKeyboardMarkup = None) -> InlineKeyboardMarkup:
    return build_markup(lang, KeyboardKey.SELECT_TASK_NAV_MENU, callback_data_param=params, source_markup=source_markup)


def with_pagination_menu(params: list[dict], text_params: list[dict], source_markup: InlineKeyboardMarkup = None) -> InlineKeyboardMarkup:
    return build_markup(None, KeyboardKey.PAGINATION_MENU, callback_data_param=params, text_params=text_params, source_markup=source_markup)


def with_bonus_task_button(params: list[dict], text_params: list[dict], source_markup: InlineKeyboardMarkup = None) -> InlineKeyboardMarkup:
    return build_markup(None, KeyboardKey.BONUS_TASK_BUTTON, callback_data_param=params, text_params=text_params, source_markup=source_markup)


def with_regenerate_captcha_button(source_markup: InlineKeyboardMarkup = None) -> InlineKeyboardMarkup:
    return build_markup(None, KeyboardKey.CAPTCHA_REGENERATE_BUTTON, source_markup=source_markup)


def get_captcha_select_menu_kbm(kaptcha_list: list[str]) -> InlineKeyboardMarkup:
    m: M = get_keyboard(KeyboardKey.CAPTCHA_SELECT_MENU, None)[0][0]
    builder = get_builder()

    for kpt in kaptcha_list:
        builder.row(build_inline_keyboard_button(m, text_param={'text': kpt}, captcha_text=kpt))

    return with_regenerate_captcha_button(builder.as_markup())


def get_public_cheque_menu_kbm(lang: Lang) -> InlineKeyboardMarkup:
    params = [
        {'type_': ChequeType.PERSONAL.value},
        {'type_': ChequeType.MULTY.value},
    ]
    return build_markup(lang, KeyboardKey.PUBLIC_CHEQUE_MENU, callback_data_param=params)


def get_cheque_action_menu_kbm(lang: Lang, cheque_type: int) -> InlineKeyboardMarkup:
    params = [
        {'type_': cheque_type},
        {'type_': cheque_type},
    ]
    return build_markup(lang, KeyboardKey.CHEQUE_ACTION_MENU, callback_data_param=params)


def get_cheque_modification_menu_kbm(lang: Lang, cheque_id: int, link: str) -> InlineKeyboardMarkup:
    url_params = [
        {'link': link},
    ]
    params = [
        {'cheque_id': cheque_id},
        {'cheque_id': cheque_id},
        {'cheque_id': cheque_id},
    ]
    return build_markup(lang, KeyboardKey.CHEQUE_MODIFICATION_MENU, url_params=url_params, callback_data_param=params)


def get_cheque_already_linked_to_user_menu_kbm(lang: Lang, cheque_id: int) -> InlineKeyboardMarkup:
    params = [
        {
            'cheque_id': cheque_id,
            'override': True
        },
        {'cheque_id': cheque_id},
    ]
    return build_markup(lang, KeyboardKey.CHEQUE_ALREADY_LINKED_TO_USER_MENU, callback_data_param=params)


def get_inline_mode_share_ref_link_button_kbm(ref_link: str) -> InlineKeyboardMarkup:
    url_params = [
        {'ref_link': ref_link},
    ]
    return build_markup(None, KeyboardKey.INLINE_MODE_SHARE_REF_LINK_BUTTON, url_params=url_params)


def get_inline_mode_cheque_activate_button(link: str) -> InlineKeyboardMarkup:
    url_params = [
        {'link': link},
    ]
    return build_markup(None, KeyboardKey.INLINE_MODE_CHEQUE_ACTIVATION_BUTTON, url_params=url_params)
