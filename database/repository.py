import logging
import uuid
from datetime import datetime
from typing import Any, Sequence

from sqlalchemy import select, func, desc, Row, update
from sqlalchemy.orm import Session

import cache
from database import User, Setting, SettingsKey, MailingMessageStatus, MailingMessage, Mailing, now, MailingStatus
from lang.lang_based_provider import Lang

logger = logging.getLogger(__name__)


def get_user_by_tg(s: Session, tg_user_id: int) -> User:
    stmt = select(User).where(User.telegram_id.__eq__(tg_user_id))
    return s.scalar(stmt)


@cache.cacheable(ttl="10m")
async def is_user_exists_by_tg(s: Session, tg_user_id: int) -> bool:
    stmt = select(User).where(User.telegram_id.__eq__(tg_user_id)).exists().select()
    return s.scalar(stmt)


@cache.cacheable(ttl="10m")
async def has_premium(s: Session, tg_user_id: int) -> bool:
    stmt = select(User.is_premium).where(User.telegram_id.__eq__(tg_user_id))
    result = s.execute(stmt)
    return result.scalar()


# def is_good_user(s: Session, user_id: int) -> bool:
#     ext = select(User) \
#         .where(User.id.__eq__(user_id)) \
#         .where(User.blocked.__eq__(False)) \
#         .where(User.deletedAt.__eq__(None)) \
#         .exists() \
#         .select()
#     result = s.execute(ext)
#     return result.scalar()


@cache.cacheable(ttl="10m")
async def is_good_user_by_tg(s: Session, tg_user_id: int) -> bool:
    ext = select(User) \
        .where(User.telegram_id.__eq__(tg_user_id)) \
        .where(User.blocked.__eq__(False)) \
        .where(User.deleted_at.__eq__(None)) \
        .where(User.is_bot_start_completed.__eq__(True)) \
        .exists() \
        .select()
    result = s.execute(ext)
    return result.scalar()


@cache.cacheable(ttl="1h")
async def is_admin(s: Session, tg_user_id: int) -> bool:
    ext = (select(User)
           .where(User.telegram_id.__eq__(tg_user_id))
           .where(User.is_admin.__eq__(True))
           .exists()
           .select())
    result = s.execute(ext)
    return result.scalar()


def save_user(s: Session, user: User) -> None:
    s.add(user)
    s.commit()


def update_user_language(s: Session, tg_user_id: int, lang: Lang) -> None:
    s.begin()
    user = get_user_by_tg(s, tg_user_id)
    user.language = lang
    s.commit()


def get_user_language(s: Session, tg_user_id: int) -> Lang:
    stmt = select(User.language).where(User.telegram_id.__eq__(tg_user_id))
    result = s.execute(stmt)
    return result.scalar()


@cache.cacheable(associate_none_as=False)
async def is_user_admin_by_tg_id(s: Session, tg_user_id: int) -> bool:
    stmt = select(User.is_admin).where(User.telegram_id.__eq__(tg_user_id))
    result = s.execute(stmt)
    return result.scalar()


def update_user_is_bot_start_completed_by_tg_id(s: Session, tg_user_id: int, val: bool) -> None:
    s.begin()
    user = get_user_by_tg(s, tg_user_id)
    user.is_bot_start_completed = val
    s.commit()


def get_setting_by_id(s: Session, key: SettingsKey) -> Setting:
    stmt = select(Setting).where(Setting.id.__eq__(key))
    result = s.execute(stmt)
    return result.scalar()


@cache.cacheable(ttl="10s")
async def get_user_referrals_count(s: Session, tg_user_id: int) -> int:
    stmt = s.query(func.count(User.telegram_id)).where(User.referred_by_id.__eq__(tg_user_id))
    return stmt.scalar()


def is_premium_user(s: Session, tg_user_id: int) -> bool:
    stmt = select(User.is_premium).where(User.telegram_id.__eq__(tg_user_id))
    return s.execute(stmt).scalar()


def update_user_premium(s: Session, tg_user_id: int, premium: bool) -> None:
    s.begin()
    user = get_user_by_tg(s, tg_user_id)
    user.is_premium = premium
    s.commit()


@cache.cacheable(ttl="6h", function_name_as_id=True)
async def get_verified_user_count(s: Session) -> int:
    stmt = (select(func.count())
            .where(User.deleted_at.__eq__(None))
            .where(User.blocked.__eq__(False))
            .where(User.is_bot_start_completed.__eq__(True)))
    return s.scalar(stmt)


def get_top_users_by_referrals(s: Session, limit: int = 10) -> Sequence[Row[tuple[Any, Any]]]:
    referred_user_alias = User.__table__.alias("referred_user")

    stmt = (
        select(
            User.telegram_id,
            func.count(referred_user_alias.c.telegram_id).label('referral_count')
        )
        .select_from(User)
        .join(referred_user_alias, referred_user_alias.c.referred_by_id == User.telegram_id)
        .group_by(User.telegram_id)
        .order_by(desc('referral_count'))
        .limit(limit)
    )
    result = s.execute(stmt).all()
    return result


def get_top_users_by_referrals_with_start_date(s: Session, start_date: datetime, limit: int = 10) -> Sequence[Row[tuple[Any, Any]]]:
    referred_user_alias = User.__table__.alias("referred_user")

    stmt = (
        select(
            User.telegram_id,
            func.count(referred_user_alias.c.telegram_id).label('referral_count')
        )
        .select_from(User)
        .join(referred_user_alias,
              (referred_user_alias.c.referred_by_id == User.telegram_id) &
              (referred_user_alias.c.created_at >= start_date))
        .group_by(User.telegram_id)
        .order_by(desc('referral_count'))
        .limit(limit)
    )
    result = s.execute(stmt).all()
    return result


def get_all_user_ids(s: Session) -> Sequence[Row[tuple[Any]]]:
    stmt = (select(User.telegram_id)
            .where(User.deleted_at.__eq__(None))
            .where(User.blocked.__eq__(False))
            .where(User.is_bot_start_completed.__eq__(True)))
    result = s.execute(stmt).all()
    return result


def update_mailing_message_status(s: Session, id_: uuid.UUID, status: MailingMessageStatus) -> bool:
    try:
        s.begin()
        stmt = (
            update(MailingMessage)
            .where(MailingMessage.id.__eq__(id_))
            .values(status=status)
        )
        s.execute(stmt)
        s.commit()
        return True
    except Exception as e:
        logger.error(f"Failed to update status for MailingMessage with ID {id_}: {e}")
        return False
    finally:
        s.close()


def update_mailing_message_statuses_by_mailing_id(s: Session, mailing_id: int, status: MailingMessageStatus) -> bool:
    try:
        s.begin()
        stmt = (
            update(MailingMessage)
            .where(MailingMessage.mailing_id.__eq__(mailing_id))
            .values(status=status)
        )
        s.execute(stmt)
        s.commit()
        return True
    except Exception as e:
        logger.error(f"Failed to update statuses for MailingMessage with mailing_id {mailing_id}: {e}")
        return False
    finally:
        s.close()


def get_mailing_message(s: Session, id_: uuid.UUID) -> MailingMessage:
    stmt = (select(MailingMessage)
            .where(MailingMessage.id.__eq__(id_)))
    result = s.execute(stmt)
    return result.scalar()


def get_mailing(s: Session, id_: int) -> Mailing:
    stmt = (
        select(Mailing)
        .where(Mailing.id.__eq__(id_))
    )
    result = s.execute(stmt)
    return result.scalar()


def get_mailing_messages_by_mailing_id(s: Session, mailing_id: int) -> Sequence[MailingMessage]:
    stmt = (
        select(MailingMessage)
        .where(MailingMessage.mailing_id.__eq__(mailing_id))
    )
    result = s.execute(stmt)
    return result.scalars().all()


def get_mailing_statistic(s: Session, mailing_id: int) -> dict["MailingMessageStatus", int]:
    stmt = (
        select(
            MailingMessage.status,
            func.count(MailingMessage.id).label('count')
        )
        .where(MailingMessage.mailing_id.__eq__(mailing_id))
        .group_by(MailingMessage.status)
    )
    result = s.execute(stmt).all()
    statistics = {status: count for status, count in result}
    return statistics


def finish_mailing(s: Session, mailing_id: int) -> None:
    try:
        stmt = (
            update(Mailing)
            .where(Mailing.id.__eq__(mailing_id))
            .values(finished_at=now(), status=MailingStatus.COMPLETED)
        )
        s.execute(stmt)
    except Exception as e:
        logger.error(f"Failed to finish mailing by id: {mailing_id}: {e}")
