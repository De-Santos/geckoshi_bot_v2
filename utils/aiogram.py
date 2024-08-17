from aiogram.types import Message, CallbackQuery


def extract_message(mc: Message | CallbackQuery) -> Message:
    if isinstance(mc, Message):
        return mc
    else:
        return mc.message
