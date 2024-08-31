from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from chat_processor.member import check_memberships
from database import get_active_tasks_page, TaskType, get_active_task, Task, TaskDoneHistory, TransactionOperation, with_session
from filters.base_filters import UserExistsFilter
from keyboard_markup.inline_user_kb import with_step_back_button, with_back_to_menu_button, with_pagination_menu, with_task_submit_button
from lang.lang_based_provider import Lang, get_message, MessageKey, format_string
from lang_based_variable import MenuToBonusCallback, PaginationMove, BonusTaskSelect, StepBack, TaskDone
from states.states import TaskStates
from transaction_manager import make_transaction_from_system, generate_trace, TraceType
from utils.task_printer import build_bonus_task_button_set, print_task

router = Router(name="bonus_router")


@router.callback_query(TaskStates.bonus_select, StepBack.filter(), UserExistsFilter())
@router.callback_query(MenuToBonusCallback.filter(), UserExistsFilter())
async def bonus_task_menu_entrypoint(query: CallbackQuery, lang: Lang, state: FSMContext) -> None:
    await bonus_task_menu(query, PaginationMove(page=1), lang, state)


@router.callback_query(PaginationMove.filter(F.disabled.__eq__(False)), UserExistsFilter())
async def bonus_task_menu(query: CallbackQuery, callback_data: PaginationMove, lang: Lang, state: FSMContext) -> None:
    await state.set_state(TaskStates.bonus_select)
    limit = 4
    pagination = await get_active_tasks_page(query.from_user.id, page=callback_data.page, task_type=TaskType.BONUS, limit=limit)

    if pagination.is_empty():
        await query.message.edit_text(text=get_message(MessageKey.BONUS_TASK_ENDED, lang),
                                      reply_markup=with_back_to_menu_button(lang), remove_source=True)
        return

    markup = build_bonus_task_button_set(pagination.items)
    next_page = callback_data.page + 1
    prev_page = callback_data.page - 1

    params = [
        {'page': prev_page, 'disabled': prev_page <= 0},
        {'page': next_page, 'disabled': next_page > pagination.total_pages}
    ]
    text_params = [
        {'cur_page': pagination.current_page, 'total_pages': pagination.total_pages},
    ]
    await query.message.edit_text(text=get_message(MessageKey.CHOOSE_BONUS, lang),
                                  reply_markup=with_back_to_menu_button(lang, with_pagination_menu(params, text_params, markup), remove_source=True))


@router.callback_query(TaskStates.bonus_select, BonusTaskSelect.filter(), UserExistsFilter())
async def select_bonus(query: CallbackQuery, callback_data: BonusTaskSelect, lang: Lang, state: FSMContext) -> None:
    await state.set_state(TaskStates.bonus_select)
    task: Task = await get_active_task(user_id=query.from_user.id, task_id=callback_data.task_id)
    if task is None:
        await bonus_task_menu_entrypoint(query, lang, state)
        return

    text, markup = print_task(lang, task)
    params = [
        {'task_id': task.id},
    ]

    await query.message.edit_text(text=text,
                                  reply_markup=with_step_back_button(lang, with_task_submit_button(lang, params, markup)),
                                  disable_web_page_preview=True)


@router.callback_query(TaskStates.bonus_select, TaskDone.filter(), UserExistsFilter())
@with_session(transaction=True)
async def process_bonus_task_done(query: CallbackQuery, callback_data: TaskDone, lang: Lang, state: FSMContext, s: AsyncSession) -> None:
    task: Task = await get_active_task(user_id=query.from_user.id, task_id=callback_data.task_id, session=s)
    if task is None:
        await bonus_task_menu_entrypoint(query, lang, state)
        return

    subscription_passed = await check_memberships(query.from_user.id, task.require_subscriptions)
    if not subscription_passed:
        await query.answer(get_message(MessageKey.TASK_DONE_UNSUCCESSFULLY, lang), show_alert=True)
        return

    s.add(TaskDoneHistory(reward=task.done_reward, user_id=query.from_user.id, task_id=task.id))
    await make_transaction_from_system(query.from_user.id, TransactionOperation.INCREMENT, task.done_reward, description="bonus task done",
                                       trace=generate_trace(TraceType.TASK_DONE, str(task.trace_uuid)), session=s, currency_type=task.coin_type)

    await query.message.answer(text=format_string(get_message(MessageKey.TASK_DONE_SUCCESSFULLY, lang), task_id=task.id))
    await bonus_task_menu_entrypoint(query, lang, state)
