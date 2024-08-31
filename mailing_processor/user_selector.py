from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import User, with_session


@with_session
async def get_all_user_ids(s: AsyncSession = None) -> list[int]:
    stmt = (select(User.telegram_id)
            .where(User.deleted_at.__eq__(None)))
    result = await s.execute(stmt)
    user_ids = [row[0] for row in result]
    return user_ids
