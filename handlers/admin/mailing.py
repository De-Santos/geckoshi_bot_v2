import datetime

import humanfriendly
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, InputMediaPhoto, InlineKeyboardButton, InlineKeyboardMarkup

import mailing_processor
from database import get_session, get_mailing, Mailing, MailingStatus, repository, MailingMessageStatus
from filters.base_filters import UserExistsFilter
from keyboard_markup.inline_user_kb import with_exit_button, get_yes_no_kbm, with_step_back_button, get_builder, get_mailing_inline_button_preview_kbm, get_mailing_add_button_or_preview_kbm, get_mailing_start_kbm, get_mailing_menu_kbm, \
    get_mailing_queue_fill_retry_kbm
from keyboard_markup.json_markup import serialize_inline_keyboard_markup, deserialize_inline_keyboard_markup
from lang.lang_based_provider import get_message, format_string
from lang_based_variable import Lang, MailingCallback, MessageKey, Yes, No, StepBack, ApproveInlineButton, AddMoreInlineButton, MailingMessagePreview, StartMailing, StopMailing, QueueFillMailingRetry, UpdateMailingStatistic
from mailing_processor import MM, fill_queue_by_mailing_id
from states.states import MailingStates

router = Router(name="admin_mailing_router")


@router.callback_query(MailingStates.has_inline_button, StepBack.filter(), UserExistsFilter())
@router.callback_query(MailingCallback.filter(), UserExistsFilter())
async def enter_mailing_message(query: CallbackQuery, lang: Lang, state: FSMContext) -> None:
    await query.message.delete()
    await state.set_state(MailingStates.enter_message)
    await query.message.answer(text=get_message(MessageKey.ADMIN_ENTER_MAILING_MESSAGE, lang),
                               reply_markup=with_exit_button(lang))


@router.message(MailingStates.has_inline_button, UserExistsFilter())
@router.message(MailingStates.enter_message, UserExistsFilter())
async def process_mailing_message(message: Message, lang: Lang, state: FSMContext) -> None:
    if message.photo:
        await message.answer("Unsupported message type.")
        return
        # file_ids: list[str] = list({photo.file_id for photo in message.photo})
        #
        # await state.update_data(file_ids=file_ids,
        #                         with_files=True)
        # text = message.caption if message.caption else None
    elif message.text:
        text = message.html_text
    else:
        await message.answer("Unsupported message type.")
        return
    await state.update_data(text=text)
    await has_inline_buttons(m=message, lang=lang, state=state)


@router.callback_query(MailingStates.preview, StepBack.filter(), UserExistsFilter())
@router.callback_query(MailingStates.enter_inline_button_text, StepBack.filter(), UserExistsFilter())
@router.message(MailingStates.has_inline_button, UserExistsFilter())
async def has_inline_buttons(m: Message | CallbackQuery, lang: Lang, state: FSMContext) -> None:
    await state.set_state(MailingStates.has_inline_button)
    await extract_message(m).answer(text=get_message(MessageKey.ADMIN_MAILING_HAS_INLINE_BUTTON, lang),
                                    reply_markup=with_step_back_button(lang, get_yes_no_kbm(lang)))


@router.callback_query(MailingStates.preview_inline_button, AddMoreInlineButton.filter(), UserExistsFilter())
@router.callback_query(MailingStates.enter_inline_button_url, StepBack.filter(), UserExistsFilter())
@router.callback_query(MailingStates.has_inline_button, Yes.filter(), UserExistsFilter())
async def request_inline_button_text(query: CallbackQuery, lang: Lang, state: FSMContext) -> None:
    await query.message.delete()
    await state.set_state(MailingStates.enter_inline_button_text)
    await query.message.answer(text=get_message(MessageKey.ADMIN_MAILING_ENTER_INLINE_BUTTON_TEXT, lang),
                               reply_markup=with_step_back_button(lang))


@router.message(MailingStates.enter_inline_button_text, UserExistsFilter())
async def process_inline_button_text(message: Message, lang: Lang, state: FSMContext) -> None:
    if not message.text:
        await message.answer("It's not a string.")
        return
    await state.update_data(inline_button_text=message.text)
    await request_inline_button_url(message, lang, state)


def extract_message(mc: Message | CallbackQuery) -> Message:
    if isinstance(mc, Message):
        return mc
    else:
        return mc.message


@router.callback_query(MailingStates.preview_inline_button, StepBack.filter(), UserExistsFilter())
async def request_inline_button_url(m: Message | CallbackQuery, lang: Lang, state: FSMContext):
    await state.set_state(MailingStates.enter_inline_button_url)
    await extract_message(m).answer(text=get_message(MessageKey.ADMIN_MAILING_ENTER_INLINE_BUTTON_URL, lang),
                                    reply_markup=with_step_back_button(lang))


@router.message(MailingStates.enter_inline_button_url, UserExistsFilter())
async def process_inline_button_url(message: Message, lang: Lang, state: FSMContext) -> None:
    if not message.text:
        await message.answer("It's not a string.")
        return
    data = await state.get_data()
    builder = get_builder()
    await state.update_data(inline_button_url=message.text)
    builder.button(text=data.get('inline_button_text'), url=message.text)
    await state.set_state(MailingStates.preview_inline_button)
    await message.answer(text=get_message(MessageKey.ADMIN_MAILING_INLINE_BUTTON_PREVIEW, lang),
                         reply_markup=with_step_back_button(lang, get_mailing_inline_button_preview_kbm(lang, builder.as_markup())))


@router.callback_query(MailingStates.preview_inline_button, ApproveInlineButton.filter(), UserExistsFilter())
async def process_add_inline_button(query: CallbackQuery, lang: Lang, state: FSMContext) -> None:
    await query.message.delete()
    data = await state.get_data()
    builder = get_builder(deserialize_inline_keyboard_markup(data.get('markup', None)).inline_keyboard)
    builder.row(InlineKeyboardButton(text=data.get('inline_button_text'), url=data.get('inline_button_url')))
    await state.update_data(markup=serialize_inline_keyboard_markup(builder.as_markup()))
    await query.message.answer(text=get_message(MessageKey.ADMIN_MAILING_ADD_INLINE_BUTTON, lang),
                               reply_markup=with_exit_button(lang, get_mailing_add_button_or_preview_kbm(lang)))


@router.callback_query(MailingStates.has_inline_button, No.filter(), UserExistsFilter())
@router.callback_query(MailingStates.preview_inline_button, MailingMessagePreview.filter(), UserExistsFilter())
async def mailing_preview(query: CallbackQuery, lang: Lang, state: FSMContext) -> None:
    await query.message.delete()
    await state.set_state(MailingStates.preview)
    data = await state.get_data()
    if data.get('with_files', False):
        media = [InputMediaPhoto(media=file_id) for file_id in data.get('file_ids', [])]
        if media:
            media[0].caption = data.get('text', None)
        message = (await query.message.answer_media_group(media=media))[0]
    else:
        message = await query.message.answer(text=data.get('text'),
                                             reply_markup=deserialize_inline_keyboard_markup(data.get('markup')))
    await query.message.answer(text=get_message(MessageKey.ADMIN_MAILING_MESSAGE_LOOKS_LIKE, lang),
                               reply_to_message_id=message.message_id,
                               reply_markup=with_exit_button(lang, with_step_back_button(lang, get_mailing_start_kbm(lang))))


@router.callback_query(MailingStates.preview, StartMailing.filter(), UserExistsFilter())
async def start_mailing(query: CallbackQuery, lang: Lang, state: FSMContext) -> None:
    await query.message.answer(get_message(MessageKey.REQUEST_PROCESSING, lang))
    data = await state.get_data()
    md, result = await mailing_processor.start_mailing(MM(
        text=data.get('text', None),
        button_markup=deserialize_inline_keyboard_markup(data.get('markup', None)),
        files=data.get('file_ids', []),
        initiator_id=query.from_user.id
    ))
    if not result:
        await queue_fill_failed(query, lang, state, md.mailing_id)
    else:
        await state.clear()
        text, markup = await get_mailing_statistic(md.mailing_id, lang)
        await query.message.answer(text=text, reply_markup=markup)


async def queue_fill_failed(query: CallbackQuery, lang: Lang, state: FSMContext, mailing_id: int) -> None:
    await state.set_state(MailingStates.queue_fill_failed)
    await query.message.answer(text=get_message(MessageKey.ADMIN_MAILING_FAILED_TO_SEND_MESSAGES_IN_QUEUE, lang),
                               reply_markup=with_exit_button(lang, get_mailing_queue_fill_retry_kbm(lang, [{'mailing_id': mailing_id}])))


@router.callback_query(StopMailing.filter(), UserExistsFilter())
async def stop_mailing(query: CallbackQuery, callback_data: StopMailing, lang: Lang) -> None:
    s = get_session()
    mailing: Mailing = get_mailing(s, callback_data.mailing_id)
    if mailing.status == MailingStatus.COMPLETED or mailing.status == MailingStatus.CANCELED:
        await query.answer(text=get_message(MessageKey.ADMIN_MAILING_CANCEL_FAILED, lang), show_alert=True)
    else:
        mailing.status = MailingStatus.CANCELED
        s.commit()
        await query.message.answer(text=format_string(get_message(MessageKey.ADMIN_MAILING_CANCEL_SUCCESSFUL, lang), mailing_id=mailing.id))
    s.close()


async def get_mailing_statistic(mailing_id: int, lang: Lang) -> (str, InlineKeyboardMarkup, bool):
    s = get_session()
    mailing: Mailing = get_mailing(s, mailing_id)
    statistic: dict["MailingMessageStatus", int] = repository.get_mailing_statistic(s, mailing_id)
    messages_processed = sum([statistic.get(MailingMessageStatus.IN_PROGRESS, 0),
                              statistic.get(MailingMessageStatus.CANCELED, 0),
                              statistic.get(MailingMessageStatus.COMPLETED, 0),
                              statistic.get(MailingMessageStatus.FAILED, 0)])
    captured = sum(statistic.values())
    messages_processed_percent = (messages_processed / captured * 100) if captured > 0 else 0
    processing_time = None
    if mailing.created_at:
        end_time = mailing.finished_at or datetime.datetime.now()
        processing_time = end_time.replace(tzinfo=datetime.timezone.utc) - mailing.created_at.replace(tzinfo=datetime.timezone.utc)
    formatted_message = format_string(
        get_message(MessageKey.ADMIN_MAILING_STATS, lang),
        mailing_id=mailing_id,
        user_captured=captured,
        status=mailing.status.name,
        successfully=statistic.get(MailingMessageStatus.COMPLETED, 0),
        in_queue=statistic.get(MailingMessageStatus.IN_QUEUE, 0),
        failed=statistic.get(MailingMessageStatus.FAILED, 0),
        canceled=statistic.get(MailingMessageStatus.CANCELED, 0),
        messages_processed=messages_processed,
        messages_processed_percents=f"{messages_processed_percent:.2f}%",
        processing_time=humanfriendly.format_timespan(processing_time.total_seconds()) if processing_time else "N/A"

    )
    inline_kbm = get_mailing_menu_kbm(lang, [{'mailing_id': mailing_id}, {'mailing_id': mailing_id}])
    update = mailing.status != MailingStatus.COMPLETED
    return formatted_message, inline_kbm, update


@router.callback_query(MailingStates.queue_fill_failed, QueueFillMailingRetry.filter(), UserExistsFilter())
async def retry_queue_fill(query: CallbackQuery, callback_data: QueueFillMailingRetry, lang: Lang, state: FSMContext) -> None:
    await query.message.answer(get_message(MessageKey.REQUEST_PROCESSING, lang))
    result = await fill_queue_by_mailing_id(callback_data.mailing_id)
    if result:
        await state.clear()
        text, markup, _ = await get_mailing_statistic(callback_data.mailing_id, lang)
        await query.message.answer(text=text, reply_markup=markup)
    else:
        await queue_fill_failed(query, lang, state, callback_data.mailing_id)


@router.callback_query(UpdateMailingStatistic.filter(), UserExistsFilter())
async def update_mailing_statistic(query: CallbackQuery, callback_data: UpdateMailingStatistic, lang: Lang) -> None:
    text, markup, update = await get_mailing_statistic(callback_data.mailing_id, lang)
    if update:
        await query.message.edit_text(text=text, reply_markup=markup)
