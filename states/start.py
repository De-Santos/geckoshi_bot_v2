from aiogram.fsm.state import StatesGroup, State


class StartStates(StatesGroup):
    language = State()
    subscription = State()
