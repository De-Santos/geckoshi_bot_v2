from aiogram.fsm.state import StatesGroup, State


class SettingsStates(StatesGroup):
    language = State()
    change_ref_pay = State()


class StartStates(StatesGroup):
    language = State()
    captcha = State()
    subscription = State()


class MailingStates(StatesGroup):
    enter_message = State()
    has_inline_button = State()
    enter_inline_button_text = State()
    enter_inline_button_url = State()
    preview_inline_button = State()
    preview = State()
    queue_fill_failed = State()


class SlotsStates(StatesGroup):
    enter_amount = State()
    play = State()


class AdminTaskStates(StatesGroup):
    menu = State()

    enter_task_id = State()
    confirm_delete = State()

    enter_type = State()
    enter_title = State()
    enter_text = State()
    enter_inline_button_text = State()
    enter_inline_button_url = State()
    preview_inline_button = State()
    enter_chat_ids = State()
    check_chat_ids = State()

    enter_done_reward = State()

    enter_expire_time = State()

    preview = State()


class TaskStates(StatesGroup):
    menu = State()
    select = State()

    bonus_select = State()


class PersonalChequeStates(StatesGroup):
    menu = State()
    action_menu = State()
    amount_require = State()
    review_amount = State()


class ChequeModifyingStates(StatesGroup):
    add_description = State()
    connect_to_user = State()

    link_to_user = State()


class TaskDoneStatisticStates(StatesGroup):
    enter_task_id = State()
