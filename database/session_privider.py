from sqlalchemy.orm import Session

from database import get_db_session


def get_session() -> Session:
    return get_db_session()
