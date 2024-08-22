import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, scoped_session

load_dotenv()

engine = create_engine(os.getenv('DATABASE_URL'),
                       pool_size=int(os.getenv('DB_ENGINE_POOL_SIZE')),
                       max_overflow=int(os.getenv('DB_ENGINE_MAX_OVERFLOW')),
                       pool_pre_ping=True,
                       pool_recycle=1800,
                       echo=bool(int(os.getenv('DB_ENGINE_ECHO'))))
SessionFactory = sessionmaker(bind=engine, autocommit=False, autoflush=False, expire_on_commit=False)
ScopedSession = scoped_session(SessionFactory)
Base = declarative_base()


def get_db_session() -> Session:
    return SessionFactory()
