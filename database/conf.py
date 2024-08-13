import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, scoped_session

load_dotenv()

engine = create_engine(
    os.getenv('DATABASE_URL'),
    pool_size=10,  # The size of the pool to be maintained, default is 5
    max_overflow=20,  # The number of connections to allow in connection pool “overflow”, default is 10
    pool_timeout=30,  # The number of seconds to wait before giving up on getting a connection from the pool
    pool_recycle=1800,  # Recycle connections after the given number of seconds, default is -1 (no recycling)
    pool_pre_ping=True,  # If True, the connection pool will test connections for liveness upon each checkout
)
SessionFactory = sessionmaker(bind=engine, autocommit=False, autoflush=False, expire_on_commit=False)
ScopedSession = scoped_session(SessionFactory)
Base = declarative_base()


def get_db_session() -> Session:
    db = SessionFactory()
    try:
        yield db
    finally:
        db.close()
