from sqlalchemy.ext.asyncio import AsyncSession

import rabbit
from database import MailingMessage, get_mailing, get_mailing_messages_by_mailing_id, update_mailing_message_statuses_by_mailing_id, MailingMessageStatus, with_session
from mailing_processor.classes import MM, MMD
from mailing_processor.mailing_orm_processor import generate_mailing, generate_mailing_messages
from mailing_processor.user_selector import get_all_user_ids
from rabbit.classes import MessageDto
from rabbit.producers import BlockingTransactionalPublisher
from utils import trywrap_async


@with_session
async def start_mailing(mm: MM, s: AsyncSession = None) -> (MMD, bool):
    user_ids = await get_all_user_ids()
    mailing = await generate_mailing(s, mm)
    messages: list["MailingMessage"] = await generate_mailing_messages(mailing, user_ids)
    result = await fill_queue(mailing, messages)
    if result:
        await update_mailing_message_statuses_by_mailing_id(mailing.id, MailingMessageStatus.IN_QUEUE, s=s)
    return MMD(mailing_id=mailing.id, users_captured=len(messages)), result


@trywrap_async(False)
async def fill_queue(mailing, messages):
    async with BlockingTransactionalPublisher(queue_name=rabbit.Queue.MESSAGE.value) as publisher:
        result: bool = await publisher.publish_messages([MessageDto(destination_id=m.destination_id,
                                                                    message=m.text,
                                                                    button_markup=mailing.markup,
                                                                    files=mailing.files,
                                                                    mailing_id=mailing.id,
                                                                    mailing_message_id=m.id,
                                                                    is_last=i == len(messages) - 1) for i, m in enumerate(messages)])
    return result


@with_session
async def fill_queue_by_mailing_id(mailing_id: int, s: AsyncSession = None) -> bool:
    mailing = await get_mailing(mailing_id, s=s)
    messages = await get_mailing_messages_by_mailing_id(mailing_id, s=s)
    result = await fill_queue(mailing, messages)
    await update_mailing_message_statuses_by_mailing_id(mailing_id, MailingMessageStatus.IN_QUEUE, s=s)
    return result
