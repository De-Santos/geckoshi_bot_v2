from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def serialize_inline_keyboard_markup(markup: InlineKeyboardMarkup) -> dict:
    return {
        "inline_keyboard": [[{"text": button.text, "url": button.url} for button in row] for row in markup.inline_keyboard]
    }


def deserialize_inline_keyboard_markup(data: dict | None) -> InlineKeyboardMarkup:
    if data is not None:
        inline_keyboard = [
            [InlineKeyboardButton(text=button["text"], url=button["url"]) for button in row]
            for row in data["inline_keyboard"]
        ]
    else:
        inline_keyboard = []
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
