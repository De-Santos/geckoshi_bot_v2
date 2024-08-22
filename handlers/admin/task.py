import logging
from datetime import timedelta
from typing import Union, List

import humanfriendly
from aiogram import Router, Bot
from aiogram.enums import ChatMemberStatus
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, InlineKeyboardButton

from database import TaskType, Task, CurrencyType, now, get_session, get_active_task_by_id, delete_task_by_id
from filters.base_filters import UserExistsFilter
from keyboard_markup.inline_user_kb import get_task_menu_kbm, get_admin_task_type_menu_kbm, with_step_back_button, with_exit_button, get_builder, get_inline_button_preview_kbm, get_add_more_buttons_or_continue_kbm, get_continue_or_retry_kbm, \
    get_save_kbm, \
    get_delete_task_menu_kbm, with_skip_button
from keyboard_markup.json_markup import deserialize_inline_keyboard_markup, serialize_inline_keyboard_markup
from lang.lang_based_provider import get_message, format_string
from lang_based_variable import Lang, TaskMenu, MessageKey, CreateTask, StartCreatingTask, StepBack, AddMoreInlineButton, ApproveInlineButton, Continue, Retry, Save, DeleteTaskMenu, DeleteTask, Skip
from states.states import AdminTaskStates
from utils.aiogram import extract_message
from utils.task_printer import print_task

router = Router(name="admin_task_router")

logger = logging.getLogger(__name__)


@router.callback_query(StepBack.filter(), AdminTaskStates.enter_type, UserExistsFilter())
@router.callback_query(TaskMenu.filter(), UserExistsFilter())
async def task_menu_handler(query: CallbackQuery, lang: Lang, state: FSMContext) -> None:
    await state.clear()
    await state.set_state(AdminTaskStates.menu)
    await query.message.answer(text=get_message(MessageKey.ADMIN_TASK_MENU, lang),
                               reply_markup=with_exit_button(lang, get_task_menu_kbm(lang)))


@router.callback_query(AdminTaskStates.menu, CreateTask.filter(), UserExistsFilter())
@router.callback_query(AdminTaskStates.menu, StepBack.filter(), UserExistsFilter())
async def request_task_type(m: CallbackQuery | Message, lang: Lang, state: FSMContext) -> None:
    await state.set_state(AdminTaskStates.enter_type)
    await extract_message(m).answer(text=get_message(MessageKey.ADMIN_TASK_TYPE_SELECT, lang),
                                    reply_markup=with_step_back_button(lang, get_admin_task_type_menu_kbm()))


@router.callback_query(StartCreatingTask.filter(), AdminTaskStates.enter_type, UserExistsFilter())
async def process_task_type(query: CallbackQuery, callback_data: StartCreatingTask, lang: Lang, state: FSMContext) -> None:
    await state.update_data(task_type=callback_data.task_type)
    await request_task_title(query, lang, state)


@router.callback_query(AdminTaskStates.enter_text, StepBack.filter(), UserExistsFilter())
async def request_task_title(query: CallbackQuery, lang: Lang, state: FSMContext) -> None:
    await state.set_state(AdminTaskStates.enter_title)
    await query.message.answer(text=get_message(MessageKey.ADMIN_TASK_TITLE_REQUEST, lang),
                               reply_markup=with_step_back_button(lang))


@router.message(AdminTaskStates.enter_title, UserExistsFilter())
async def process_task_title(message: Message, lang: Lang, state: FSMContext) -> None:
    await state.update_data(title=message.html_text)
    await request_task_text(message, lang, state)


@router.callback_query(AdminTaskStates.enter_inline_button_text, StepBack.filter(), UserExistsFilter())
async def request_task_text(m: Message | CallbackQuery, lang, state):
    await state.set_state(AdminTaskStates.enter_text)
    await extract_message(m).answer(text=get_message(MessageKey.ADMIN_TASK_TEXT_REQUEST, lang),
                                    reply_markup=with_step_back_button(lang))


@router.message(AdminTaskStates.enter_text, UserExistsFilter())
async def process_task_text(message: Message, lang: Lang, state: FSMContext) -> None:
    await state.update_data(text=message.html_text)
    await request_inline_button_text(message, lang, state)


@router.callback_query(AdminTaskStates.preview_inline_button, AddMoreInlineButton.filter(), UserExistsFilter())
@router.callback_query(AdminTaskStates.enter_inline_button_url, StepBack.filter(), UserExistsFilter())
async def request_inline_button_text(m: CallbackQuery | Message, lang: Lang, state: FSMContext) -> None:
    await state.set_state(AdminTaskStates.enter_inline_button_text)
    await extract_message(m).answer(text=get_message(MessageKey.ADMIN_ENTER_INLINE_BUTTON_TEXT, lang),
                                    reply_markup=with_step_back_button(lang))


@router.message(AdminTaskStates.enter_inline_button_text, UserExistsFilter())
async def process_inline_button_text(message: Message, lang: Lang, state: FSMContext) -> None:
    if not message.text:
        await message.answer("It's not a string.")
        return
    await state.update_data(inline_button_text=message.text)
    await request_inline_button_url(message, lang, state)


@router.callback_query(AdminTaskStates.preview_inline_button, StepBack.filter(), UserExistsFilter())
async def request_inline_button_url(m: Message | CallbackQuery, lang: Lang, state: FSMContext):
    await state.set_state(AdminTaskStates.enter_inline_button_url)
    await extract_message(m).answer(text=get_message(MessageKey.ADMIN_ENTER_INLINE_BUTTON_URL, lang),
                                    reply_markup=with_step_back_button(lang))


@router.message(AdminTaskStates.enter_inline_button_url, UserExistsFilter())
async def process_inline_button_url(message: Message, lang: Lang, state: FSMContext) -> None:
    if not message.text:
        await message.answer("It's not a string.")
        return
    data = await state.get_data()
    builder = get_builder()
    await state.update_data(inline_button_url=message.text)
    builder.button(text=data.get('inline_button_text'), url=message.text)
    await state.set_state(AdminTaskStates.preview_inline_button)
    await message.answer(text=get_message(MessageKey.ADMIN_INLINE_BUTTON_PREVIEW, lang),
                         reply_markup=with_step_back_button(lang, get_inline_button_preview_kbm(lang, builder.as_markup())))


@router.callback_query(AdminTaskStates.preview_inline_button, ApproveInlineButton.filter(), UserExistsFilter())
async def process_add_inline_button(query: CallbackQuery, lang: Lang, state: FSMContext) -> None:
    await query.message.delete()
    data = await state.get_data()
    builder = get_builder(deserialize_inline_keyboard_markup(data.get('markup', None)).inline_keyboard)
    builder.row(InlineKeyboardButton(text=data.get('inline_button_text'), url=data.get('inline_button_url')))
    await state.update_data(markup=serialize_inline_keyboard_markup(builder.as_markup()))
    await query.message.answer(text=get_message(MessageKey.ADMIN_ADD_INLINE_BUTTON, lang),
                               reply_markup=with_exit_button(lang, get_add_more_buttons_or_continue_kbm(lang)))


@router.callback_query(AdminTaskStates.enter_expire_time, StepBack.filter(), UserExistsFilter())
@router.callback_query(AdminTaskStates.check_chat_ids, Retry.filter(), UserExistsFilter())
@router.callback_query(AdminTaskStates.preview_inline_button, Continue.filter(), UserExistsFilter())
async def request_required_chat_subscriptions(query: CallbackQuery, lang: Lang, state: FSMContext) -> None:
    await state.set_state(AdminTaskStates.enter_chat_ids)
    await query.message.answer(text=get_message(MessageKey.ADMIN_TASK_CHAT_SUBSCRIPTIONS_REQUIRE_REQUEST, lang),
                               reply_markup=with_exit_button(lang, with_skip_button(lang)))


async def parse_chat_ids(chat_ids_str: str, message: Message) -> List[Union[str, int]]:
    chat_ids = []

    # Split the input string by commas only if commas are present
    raw_ids = [chat_ids_str.strip()] if ',' not in chat_ids_str else chat_ids_str.split(',')

    for raw_id in raw_ids:
        raw_id = raw_id.strip()

        if raw_id.startswith('@'):
            chat_ids.append(raw_id)
        else:
            try:
                chat_ids.append(int(raw_id))
            except ValueError:
                await message.answer(f"Invalid ID format: {raw_id}")

    return chat_ids


async def validate_bot_in_chats(bot: Bot, chat_ids: List[Union[str, int]]) -> dict[Union[str, int], str]:
    results = {}

    for chat_id in chat_ids:
        try:
            bot_member = await bot.get_chat_member(chat_id, bot.id)
            bot_has_access = bot_member.status in [
                ChatMemberStatus.ADMINISTRATOR,
                ChatMemberStatus.CREATOR
            ]

            results[chat_id] = f"has access: {bot_has_access}"
        except Exception as e:
            results[chat_id] = f"error: {e}"
            logger.error(f"Error checking chat {chat_id}: {e}")

    return results


@router.message(AdminTaskStates.enter_chat_ids, UserExistsFilter())
async def process_chat_ids(message: Message, bot: Bot, lang: Lang, state: FSMContext) -> None:
    await message.answer(text=get_message(MessageKey.REQUEST_PROCESSING, lang))
    await state.set_state(AdminTaskStates.check_chat_ids)
    row = "{chat_id} - {result}\n"
    result = ""
    chat_ids: list[int] = await parse_chat_ids(message.text, message)
    await state.update_data(chat_ids=chat_ids)
    for ci, r in (await validate_bot_in_chats(bot, chat_ids)).items():
        result += row.format(chat_id=ci, result=r)
    await message.answer(text=f"Check channels\n\n{result}",
                         reply_markup=with_exit_button(lang, get_continue_or_retry_kbm(lang)))


@router.callback_query(AdminTaskStates.enter_chat_ids, Skip.filter(), UserExistsFilter())
@router.callback_query(AdminTaskStates.enter_expire_time, StepBack.filter(), UserExistsFilter())
@router.callback_query(AdminTaskStates.check_chat_ids, Continue.filter(), UserExistsFilter())
async def request_extra_data(query: CallbackQuery, lang: Lang, state: FSMContext) -> None:
    task_type = (await state.get_data())['task_type']
    if task_type == TaskType.TIME_BASED.value:
        await request_expire_time(query, lang, state)
    if task_type == TaskType.BONUS.value:
        await request_done_reward(query.message, lang, state)


async def request_expire_time(m: CallbackQuery | Message, lang: Lang, state: FSMContext) -> None:
    await state.set_state(AdminTaskStates.enter_expire_time)
    await extract_message(m).answer(text=get_message(MessageKey.ADMIN_TASK_EXPIRE_TIME_REQUEST, lang),
                                    reply_markup=with_step_back_button(lang))


@router.message(AdminTaskStates.enter_expire_time, UserExistsFilter())
async def process_expire_time(message: Message, lang: Lang, state: FSMContext) -> None:
    await state.set_state(AdminTaskStates.enter_expire_time)
    try:
        await state.update_data(expires_at=humanfriendly.parse_timespan(message.text))
    except Exception as e:
        msg = f"Failed to convert str: {message.text} to datetime, error - {str(e)}"
        logger.error(msg)
        await message.answer(text=msg)
        return
    await request_done_reward(message, lang, state)


async def request_done_reward(message: Message, lang: Lang, state: FSMContext):
    await state.set_state(AdminTaskStates.enter_done_reward)
    if TaskType((await state.get_data()).get('task_type')) == TaskType.POOL_BASED:
        await message.answer(text=get_message(MessageKey.ADMIN_TASK_BMEME_DONE_REWARD_REQUEST, lang),
                             reply_markup=with_step_back_button(lang))
    else:
        await message.answer(text=get_message(MessageKey.ADMIN_TASK_GMEME_DONE_REWARD_REQUEST, lang),
                             reply_markup=with_step_back_button(lang))


@router.message(AdminTaskStates.enter_done_reward, UserExistsFilter())
async def process_done_reward(message: Message, lang: Lang, state: FSMContext) -> None:
    await state.update_data(done_reward=int(message.text))
    await preview(message, lang, state)


async def create_task_from_state_data(state: FSMContext, created_by_id: int = None) -> Task:
    data = await state.get_data()

    task_type = TaskType(data.get('task_type'))
    title = data.get('title')
    text = data.get('text')
    markup = data.get('markup', {})
    require_subscriptions = data.get('chat_ids', [])
    expires_at = now() + timedelta(seconds=data.get('expires_at')) if data.get('expires_at') is not None else None
    done_limit = data.get('done_limit')
    coin_pool = data.get('coin_pool')
    done_reward = data.get('done_reward')

    coin_type = CurrencyType.BMEME if task_type == TaskType.POOL_BASED else CurrencyType.GMEME

    if task_type == TaskType.POOL_BASED:
        done_limit = coin_pool // done_reward

    new_task = Task(
        type=task_type,
        title=title,
        text=text,
        markup=markup,
        require_subscriptions=require_subscriptions,
        coin_type=coin_type,
        done_limit=done_limit,
        coin_pool=coin_pool,
        done_reward=done_reward,
        created_by_id=created_by_id,
        expires_at=expires_at
    )

    return new_task


async def preview(m: CallbackQuery | Message, lang: Lang, state: FSMContext):
    await state.set_state(AdminTaskStates.preview)
    message = extract_message(m)
    task = await create_task_from_state_data(state, message.from_user.id)
    text, markup = print_task(lang, task)
    await message.answer(text=text, reply_markup=get_save_kbm(lang, markup))


@router.callback_query(AdminTaskStates.preview, Save.filter(), UserExistsFilter())
async def save(query: CallbackQuery, lang: Lang, state: FSMContext) -> None:
    s = get_session()
    task = await create_task_from_state_data(state, query.from_user.id)
    s.add(task)
    s.commit()
    await state.clear()
    await query.message.answer(text=format_string(get_message(MessageKey.ADMIN_TASK_SAVED_SUCCESSFULLY, lang),
                                                  task_id=task.id))
    s.close()


@router.callback_query(AdminTaskStates.menu, DeleteTaskMenu.filter(), UserExistsFilter())
async def request_task_id(m: CallbackQuery | Message, lang: Lang, state: FSMContext) -> None:
    await state.set_state(AdminTaskStates.enter_task_id)
    await extract_message(m).answer(text=get_message(MessageKey.ADMIN_TASK_ID_REQUEST, lang),
                                    reply_markup=with_exit_button(lang))


@router.message(AdminTaskStates.enter_task_id, UserExistsFilter())
async def process_task_id(message: Message, lang: Lang, state: FSMContext) -> None:
    task = get_active_task_by_id(get_session(), int(message.text))
    text, markup = print_task(lang, task)
    await state.set_state(AdminTaskStates.confirm_delete)
    m = await message.answer(text=text,
                             reply_markup=markup)
    await message.answer(text=get_message(MessageKey.ADMIN_CONFIRM_TASK_DELETE, lang),
                         reply_to_message_id=m.message_id,
                         reply_markup=with_exit_button(lang, get_delete_task_menu_kbm(lang, task.id)))


@router.callback_query(AdminTaskStates.confirm_delete, DeleteTask.filter(), UserExistsFilter())
async def process_task_deletion(m: CallbackQuery | Message, callback_data: DeleteTask, lang: Lang, state: FSMContext) -> None:
    delete_task_by_id(get_session(), callback_data.task_id, m.from_user.id)
    await state.clear()
    await extract_message(m).answer(text=get_message(MessageKey.ADMIN_TASK_DELETED_SUCCESSFULLY, lang))
