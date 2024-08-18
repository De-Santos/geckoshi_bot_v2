import datetime

import humanfriendly
from aiogram.types import InlineKeyboardMarkup

from database import Task, TaskType, now
from keyboard_markup.json_markup import deserialize_inline_keyboard_markup
from lang.lang_based_provider import get_message, format_string
from lang_based_variable import MessageKey, Lang


def print_task(lang: Lang, task: Task) -> (str, InlineKeyboardMarkup):
    if task.type == TaskType.TIME_BASED:
        return (format_string(get_message(MessageKey.TIME_BASED_TASK, lang),
                              task_id=task.id,
                              title=task.title,
                              text=task.text,
                              done_reward=task.done_reward,
                              expires_in=humanfriendly.format_timespan(task.expires_at.replace(tzinfo=datetime.UTC) - now())),

                deserialize_inline_keyboard_markup(task.markup))
