from datetime import datetime
from typing import Any, Sequence

from sqlalchemy import select, func, desc, Row
from sqlalchemy.orm import Session

import cache
from database import User, Setting, SettingsKey
from lang.lang_based_provider import Lang


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
        .where(User.deletedAt.__eq__(None)) \
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
            .where(User.deletedAt.__eq__(None))
            .where(User.blocked.__eq__(False))
            .where(User.is_bot_start_completed.__eq__(True)))
    return s.scalar(stmt)


def get_top_users_by_referrals(db: Session, limit: int = 10) -> Sequence[Row[tuple[Any, Any]]]:
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
    result = db.execute(stmt).all()
    return result


def get_top_users_by_referrals_with_start_date(db: Session, start_date: datetime, limit: int = 10) -> Sequence[Row[tuple[Any, Any]]]:
    referred_user_alias = User.__table__.alias("referred_user")

    stmt = (
        select(
            User.telegram_id,
            func.count(referred_user_alias.c.telegram_id).label('referral_count')
        )
        .select_from(User)
        .join(referred_user_alias,
              (referred_user_alias.c.referred_by_id == User.telegram_id) &
              (referred_user_alias.c.createdAt >= start_date))
        .group_by(User.telegram_id)
        .order_by(desc('referral_count'))
        .limit(limit)
    )
    result = db.execute(stmt).all()
    return result
