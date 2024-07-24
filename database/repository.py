from sqlalchemy import select
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
        .exists() \
        .select()
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
