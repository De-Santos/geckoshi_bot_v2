from sqlalchemy import select

from database import User, get_session


def get_all_user_ids() -> list[int]:
    s = get_session()
    stmt = (select(User.telegram_id)
            .where(User.deleted_at.__eq__(None)))
    result = s.execute(stmt)
    user_ids = [row[0] for row in result]
    return user_ids
