from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db_session


def get_session() -> AsyncSession:
    return get_db_session()
