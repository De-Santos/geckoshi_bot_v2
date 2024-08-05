from aiogram.fsm.state import StatesGroup, State


class SettingsStates(StatesGroup):
    language = State()
    change_ref_pay = State()
