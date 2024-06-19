from sqlalchemy.orm import Session

from database import engine


def get_session() -> Session:
    return Session(engine)
