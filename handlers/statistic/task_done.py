from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from tabulate import tabulate

from database import get_tasks_statistics, get_task_statistic
from filters.base_filters import UserExistsFilter
from lang.lang_based_provider import Lang, format_string, get_message
from lang_based_variable import TaskDoneStatistic, MessageKey, TaskDoneStatisticMenu
from states.states import TaskDoneStatisticStates

router = Router(name="task_done_router")


@router.callback_query(TaskDoneStatistic.filter(), UserExistsFilter())
async def process_statistic(query: CallbackQuery, lang: Lang) -> None:
    statistic = await get_tasks_statistics()
    text_table = generate_text_table(statistic)
    await query.message.answer(text=format_string(get_message(MessageKey.TASK_DONE_STATISTIC, lang),
                                                  text_table=text_table))


@router.callback_query(TaskDoneStatisticMenu.filter(), UserExistsFilter())
async def process_statistic_by_id(query: CallbackQuery, lang: Lang, state: FSMContext) -> None:
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
    text_table = generate_text_table(statistic)
    await message.answer(text=format_string(get_message(MessageKey.TASK_DONE_STATISTIC, lang),
                                            text_table=text_table))


def generate_text_table(data) -> str:
    return tabulate(data, headers=['task id', 'done count'], tablefmt='grid')
