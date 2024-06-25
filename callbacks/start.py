from aiogram.filters.callback_data import CallbackData

from lang.lang_based_text_provider import Lang, KeyboardKey


class LangSetCallback(CallbackData, prefix="start-set-lang"):
    lang: Lang


class CheckStartMembershipCallback(CallbackData, prefix="check-start-membership"):
    kbk: KeyboardKey
    lang: Lang
