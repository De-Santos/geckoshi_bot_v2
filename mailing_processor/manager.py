import rabbit
from database import get_session, MailingMessage, get_mailing, get_mailing_messages_by_mailing_id, update_mailing_message_statuses_by_mailing_id, MailingMessageStatus
from mailing_processor.classes import MM, MMD
from mailing_processor.mailing_orm_processor import generate_mailing, generate_mailing_messages
from mailing_processor.user_selector import get_all_user_ids
from rabbit.classes import MessageDto
from rabbit.producers import BlockingTransactionalPublisher
from utils import trywrap_async


async def start_mailing(mm: MM) -> (MMD, bool):
    user_ids = get_all_user_ids()
    s = get_session()
    mailing = generate_mailing(s, mm)
    messages: list["MailingMessage"] = generate_mailing_messages(mailing, user_ids)
    result = await fill_queue(mailing, messages)
    if result:
        update_mailing_message_statuses_by_mailing_id(s, mailing.id, MailingMessageStatus.IN_QUEUE)
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


async def fill_queue_by_mailing_id(mailing_id: int) -> bool:
    s = get_session()
    mailing = get_mailing(s, mailing_id)
    messages = get_mailing_messages_by_mailing_id(s, mailing_id)
    result = await fill_queue(mailing, messages)
    update_mailing_message_statuses_by_mailing_id(s, mailing_id, MailingMessageStatus.IN_QUEUE)
    return result
