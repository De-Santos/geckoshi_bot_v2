from sqlalchemy import select
from sqlalchemy.orm import Session

import cache
from database import User


def get_user_by_tg(s: Session, tg_user_id: int) -> User:
    stmt = select(User).where(User.telegram_id.__eq__(tg_user_id))
    return s.scalar(stmt)


@cache.cacheable(ttl="10m")
async def is_user_exists_by_tg(s: Session, tg_user_id: int) -> bool:
    stmt = select(User).where(User.telegram_id.__eq__(tg_user_id)).exists().select()
    return s.scalar(stmt)


def is_good_user(s: Session, user_id: int) -> bool:
    ext = select(User) \
        .where(User.id.__eq__(user_id)) \
        .where(User.blocked.__eq__(False)) \
        .where(User.deletedAt.__eq__(None)) \
        .exists() \
        .select()
    result = s.execute(ext)
    return result.scalar()


def save_user(s: Session, user: User) -> None:
    s.add(user)
    s.commit()
