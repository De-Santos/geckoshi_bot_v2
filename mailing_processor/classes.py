from aiogram.types import InlineKeyboardMarkup

from keyboard_markup.json_markup import serialize_inline_keyboard_markup


class MM:
    text: str | None
    button_markup: InlineKeyboardMarkup | None
    files: list[str] = []
    initiator_id: int

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def serialize_button_markup(self):
        return serialize_inline_keyboard_markup(self.button_markup)


class MMD:
    mailing_id: int
    users_captured: int

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
