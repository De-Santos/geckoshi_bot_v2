import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, scoped_session

load_dotenv()

engine = create_engine(os.getenv('DATABASE_URL'), echo=False)
SessionFactory = sessionmaker(bind=engine, autocommit=False, autoflush=False, expire_on_commit=False)
ScopedSession = scoped_session(SessionFactory)
Base = declarative_base()


def get_db_session() -> Session:
    return SessionFactory()
