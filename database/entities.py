import datetime
import uuid
from typing import List, Optional

from sqlalchemy import Column, DateTime, ForeignKey, BigInteger, Enum as SQLEnum, Numeric
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base
from database.enums import TransactionOperation, TransactionStatus


class BaseInfo:
    createdAt = Column(DateTime, default=datetime.datetime.now(datetime.UTC))
    deletedAt = Column(DateTime, default=None)


class User(BaseInfo, Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(type_=BigInteger, primary_key=True)
    telegram_id: Mapped[int] = mapped_column(type_=BigInteger, unique=True, index=True)
    balance: Mapped[int] = mapped_column(type_=Numeric, default=0)
    referred_by_id: Mapped[Optional[int]] = mapped_column(ForeignKey('users.id'), type_=BigInteger)
    blocked: Mapped[bool] = mapped_column(default=False)

    referrals: Mapped[List["User"]] = relationship("User", backref="referred_by", remote_side='User.id')


class Transaction(Base):
    __tablename__ = 'transactions'
    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    operation: Mapped[TransactionOperation] = mapped_column(SQLEnum(TransactionOperation), nullable=False)
    amount: Mapped[int] = mapped_column(type_=BigInteger)
    status: Mapped[TransactionStatus] = mapped_column(SQLEnum(TransactionStatus))
    description: Mapped[str] = mapped_column()
    createdAt = Column(DateTime, default=datetime.datetime.now(datetime.UTC))
    abortedAt = Column(DateTime)
