from aiogram.fsm.state import StatesGroup, State


class SettingsStates(StatesGroup):
    language = State()
    change_ref_pay = State()


class StartStates(StatesGroup):
    language = State()
    subscription = State()


class MailingStates(StatesGroup):
    enter_message = State()
    has_inline_button = State()
    enter_inline_button_text = State()
    enter_inline_button_url = State()
    preview_inline_button = State()
    preview = State()
    queue_fill_failed = State()
