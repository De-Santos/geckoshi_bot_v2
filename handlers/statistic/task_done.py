from datetime import timedelta

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from tabulate import tabulate

from database import get_tasks_statistics, get_task_statistic, Task, now
from filters.base_filters import UserExistsFilter
from lang.lang_based_provider import Lang, format_string, get_message
from lang_based_variable import TaskDoneStatistic, MessageKey, TaskDoneStatisticMenu
from states.states import TaskDoneStatisticStates

router = Router(name="task_done_router")


@router.callback_query(TaskDoneStatistic.filter(), UserExistsFilter())
async def process_statistic(query: CallbackQuery, lang: Lang) -> None:
    await query.message.delete()
    statistic = await get_tasks_statistics()
    text_table = generate_text_table(statistic)
    await query.message.answer(text=format_string(get_message(MessageKey.TASK_DONE_STATISTIC, lang),
                                                  text_table=text_table))


@router.callback_query(TaskDoneStatisticMenu.filter(), UserExistsFilter())
async def process_statistic_by_id(query: CallbackQuery, lang: Lang, state: FSMContext) -> None:
    await query.message.delete()
    await state.set_state(TaskDoneStatisticStates.enter_task_id)

    await _require_task_id(query.message, lang)


async def _require_task_id(message: Message, lang: Lang):
    await message.answer(text=get_message(MessageKey.ADMIN_TASK_ID_REQUEST, lang))


@router.message(TaskDoneStatisticStates.enter_task_id, UserExistsFilter())
async def handle_task_id(message: Message, lang: Lang) -> None:
    id_ = message.text.strip()
    if not id_.isdigit():
        await _require_task_id(message, lang)
        return
    id_ = int(id_)

    statistic = await get_task_statistic(id_)
    if statistic is None:
        return
    task, count = statistic
    task_duration = calculate_task_duration(task)
    text_table = generate_expanded_text_table([[task.id, count, format_timedelta(task_duration)]])
    await message.answer(text=format_string(get_message(MessageKey.TASK_DONE_STATISTIC, lang),
                                            text_table=text_table))


def calculate_task_duration(t: Task) -> timedelta:
    if now() < t.expires_at:
        return now() - t.created_at
    else:
        return t.created_at - t.expires_at if t.deleted_at is None else t.deleted_at


def generate_expanded_text_table(data) -> str:
    return tabulate(data, headers=['task id', 'done count', 'dur'], tablefmt='grid', maxcolwidths=15)


def generate_text_table(data) -> str:
    return tabulate(data, headers=['task id', 'done count'], tablefmt='grid')


def format_statistic_timedelta(statistic) -> None:
    for i in range(len(statistic)):
        # Convert Row object to a list to make it mutable
        statistic[i] = list(statistic[i])
        statistic[i][2] = format_timedelta(statistic[i][2])


def format_timedelta(td: timedelta) -> str:
    ts = int(td.total_seconds())
    days = ts // (24 * 3600)
    hours = (ts % (24 * 3600)) // 3600
    minutes = (ts % 3600) // 60

    return f"{days}d {hours:02}h {minutes:02}m"
