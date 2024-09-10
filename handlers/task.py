from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from chat_processor.member import check_memberships
from database import get_active_tasks_page, TaskType, Task, get_active_task_by_id, check_task_is_done, TaskDoneHistory, TransactionOperation, with_session
from filters.base_filters import UserExistsFilter
from keyboard_markup.inline_user_kb import with_step_back_button, with_back_to_menu_button, get_select_task_nav_menu_kbm
from lang.lang_based_provider import Lang, get_message, MessageKey, format_string
from lang_based_variable import MenuToTasksCallback, TaskSelect, StepBack, TaskDone
from states.states import TaskStates
from transaction_manager import TraceType, generate_trace, make_transaction_from_system
from utils.task_printer import print_task

router = Router(name="task_router")


@router.callback_query(TaskStates.select, StepBack.filter(), UserExistsFilter())
@router.callback_query(MenuToTasksCallback.filter(), UserExistsFilter())
async def task_menu(query: CallbackQuery, lang: Lang, state: FSMContext) -> None:
    # Temporary
    # await query.message.delete()
    # await state.set_state(TaskStates.menu)
    # await query.message.answer(text=get_message(MessageKey.CHOOSE_TASK_TYPE, lang),
    #                            reply_markup=get_task_type_menu_kbm(lang))
    #
    await select_task(query, TaskSelect(task_type=TaskType.TIME_BASED.value, page=1), lang, state)


@router.callback_query(TaskStates.select, TaskSelect.filter(F.disabled.__eq__(False)), UserExistsFilter())
@router.callback_query(TaskStates.menu, TaskSelect.filter(F.disabled.__eq__(False)), UserExistsFilter())
async def select_task(query: CallbackQuery, callback_data: TaskSelect, lang: Lang, state: FSMContext) -> None:
    await state.set_state(TaskStates.select)
    pagination = await get_active_tasks_page(page=callback_data.page, task_type=TaskType(callback_data.task_type), user_id=query.from_user.id)
    task: Task = pagination.get_one()
    if task is None:
        await query.message.edit_text(text=get_message(MessageKey.TASK_ENDED, lang),
                                      reply_markup=with_back_to_menu_button(lang, with_step_back_button(lang), remove_source=True))
        return

    text, markup = print_task(lang, task)
    next_offset = callback_data.page + 1
    prev_page = callback_data.page - 1

    done_params = [
        {'task_id': task.id},
    ]
    params = [
        {'task_type': callback_data.task_type, 'page': prev_page, 'disabled': prev_page <= 0},
        {'task_type': callback_data.task_type, 'page': next_offset, 'disabled': next_offset > pagination.total_pages}
    ]
    await query.message.edit_text(text=text,
                                  reply_markup=with_back_to_menu_button(lang, get_select_task_nav_menu_kbm(lang, done_params, params, markup), remove_source=True),
                                  disable_web_page_preview=True)


@router.callback_query(TaskStates.select, TaskDone.filter(), UserExistsFilter())
@with_session(transaction=True)
async def process_task_done(query: CallbackQuery, callback_data: TaskDone, lang: Lang, state: FSMContext, s: AsyncSession = None) -> None:
    task: Task = await get_active_task_by_id(callback_data.task_id, session=s)
    done = await check_task_is_done(task.id, query.from_user.id, s=s)

    task_type = task.type.value

    if done:
        await query.answer(get_message(MessageKey.TASK_ALREADY_HAS_DONE, lang), show_alert=True)
        return

    subscription_passed = await check_memberships(query.from_user.id, task.require_subscriptions)
    if not subscription_passed:
        await query.answer(get_message(MessageKey.TASK_DONE_UNSUCCESSFULLY, lang), show_alert=True)
        return

    s.add(TaskDoneHistory(reward=task.done_reward, user_id=query.from_user.id, task_id=task.id))
    await make_transaction_from_system(query.from_user.id, TransactionOperation.INCREMENT, task.done_reward, description="task done",
                                       trace=generate_trace(TraceType.TASK_DONE, str(task.trace_uuid)), session=s, currency_type=task.coin_type)

    await query.message.answer(text=format_string(get_message(MessageKey.TASK_DONE_SUCCESSFULLY, lang), task_id=task.id))
    await select_task(query, TaskSelect(task_type=task_type, page=1), lang, state)
