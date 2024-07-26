import datetime
import uuid
from typing import List, Optional

from sqlalchemy import Column, DateTime, ForeignKey, BigInteger, Enum as SQLEnum, Numeric
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base
from database.enums import TransactionOperation, TransactionStatus, SettingsKey
from lang.lang_based_provider import Lang


class BaseInfo:
    createdAt = Column(DateTime, default=datetime.datetime.now(datetime.UTC))
    deletedAt = Column(DateTime, default=None)


class User(BaseInfo, Base):
    __tablename__ = 'users'

    telegram_id: Mapped[int] = mapped_column(type_=BigInteger, primary_key=True)
    balance: Mapped[int] = mapped_column(type_=Numeric, default=0)
    referred_by_id: Mapped[Optional[int]] = mapped_column(ForeignKey('users.telegram_id'), type_=BigInteger)
    blocked: Mapped[bool] = mapped_column(default=False)
    language: Mapped[Lang] = mapped_column(SQLEnum(Lang), default=Lang.EN)
    is_admin: Mapped[bool] = mapped_column(default=False)
    is_bot_start_completed: Mapped[bool] = mapped_column(default=False)

    referrals: Mapped[List["User"]] = relationship("User", backref="referred_by", remote_side='User.telegram_id')


class Transaction(Base):
    __tablename__ = 'transactions'

    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    operation: Mapped[TransactionOperation] = mapped_column(SQLEnum(TransactionOperation), nullable=False)
    amount: Mapped[int] = mapped_column(type_=BigInteger)
    balance_before: Mapped[int] = mapped_column(type_=BigInteger, nullable=False)
    balance_after: Mapped[int] = mapped_column(type_=BigInteger, nullable=False)
    status: Mapped[TransactionStatus] = mapped_column(SQLEnum(TransactionStatus))
    description: Mapped[str] = mapped_column()
    destination_id: Mapped[int] = mapped_column(ForeignKey('users.telegram_id'), type_=BigInteger)
    destination: Mapped[User] = relationship("User", foreign_keys=[destination_id])
    created_by_id: Mapped[int] = mapped_column(ForeignKey('users.telegram_id'), type_=BigInteger)
    created_by: Mapped[User] = relationship("User", foreign_keys=[created_by_id])
    createdAt = Column(DateTime, default=datetime.datetime.now(datetime.UTC))
    abortedAt = Column(DateTime)


class Settings(Base):
    __tablename__ = 'settings'

    id: Mapped[SettingsKey] = mapped_column(SQLEnum(SettingsKey), primary_key=True)
    int_val: Mapped[int] = mapped_column(type_=BigInteger, nullable=True)
    str_val: Mapped[str] = mapped_column(nullable=True)
