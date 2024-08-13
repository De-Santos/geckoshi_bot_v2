import logging

from sqlalchemy.orm import Session

from database import Mailing, get_session, MailingStatus, MailingMessage, MailingMessageStatus
from mailing_processor.classes import MM


def generate_mailing(s: Session, mm: MM) -> Mailing:
    s.begin()
    mailing = Mailing(
        files=mm.files,
        text=mm.text,
        markup=mm.serialize_button_markup(),
        status=MailingStatus.IN_PROGRESS,
        created_by_id=mm.initiator_id
    )
    s.add(mailing)
    s.commit()
    s.expunge_all()
    return mailing


def generate_mailing_messages(mailing: Mailing, user_ids: list[int]) -> list["MailingMessage"]:
    s = get_session()
    s.begin()
    messages: list["MailingMessage"] = []
    for user_id in user_ids:
        messages.append(MailingMessage(
            text=mailing.text,
            status=MailingMessageStatus.IN_PROGRESS,
            destination_id=user_id,
            mailing_id=mailing.id
        ))
    try:
        s.add_all(messages)
        s.commit()
    except Exception as e:
        s.rollback()
        logging.error(f"Error occurred: {e}")
    finally:
        s.expunge_all()
        s.close()

    return messages
