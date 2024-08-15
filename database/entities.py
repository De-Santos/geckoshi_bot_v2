import datetime
import uuid
from typing import List, Optional

from sqlalchemy import Column, DateTime, ForeignKey, BigInteger, Enum as SQLEnum, Numeric, Text, func
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base
from database.enums import TransactionOperation, TransactionStatus, SettingsKey, TransactionType, TransactionInitiatorType, MailingStatus, MailingMessageStatus, BetType
from lang.lang_based_provider import Lang


def now() -> datetime.datetime:
    return datetime.datetime.now(datetime.UTC)


class User(Base):
    __tablename__ = 'users'

    telegram_id: Mapped[int] = mapped_column(type_=BigInteger, primary_key=True)
    balance: Mapped[int] = mapped_column(type_=Numeric, default=0)
    referred_by_id: Mapped[Optional[int]] = mapped_column(ForeignKey('users.telegram_id'), type_=BigInteger)
    blocked: Mapped[bool] = mapped_column(default=False)
    language: Mapped[Lang] = mapped_column(SQLEnum(Lang), default=Lang.EN)
    is_admin: Mapped[bool] = mapped_column(default=False, nullable=False)
    is_premium: Mapped[bool] = mapped_column(default=False, nullable=False)
    is_bot_start_completed: Mapped[bool] = mapped_column(default=False)
    created_at = mapped_column("created_at", DateTime, default=now, index=True)
    deleted_at = Column(DateTime, default=None)

    referrals: Mapped[List["User"]] = relationship("User", backref="referred_by", remote_side='User.telegram_id')


class Transaction(Base):
    __tablename__ = 'transactions'

    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    operation: Mapped[TransactionOperation] = mapped_column(SQLEnum(TransactionOperation), nullable=False)
    type: Mapped[TransactionType] = mapped_column(SQLEnum(TransactionType), nullable=False)
    amount: Mapped[int] = mapped_column(type_=BigInteger)
    destination_balance_before: Mapped[int] = mapped_column(type_=BigInteger, nullable=False)
    destination_balance_after: Mapped[int] = mapped_column(type_=BigInteger, nullable=False)
    source_balance_before: Mapped[int] = mapped_column(type_=BigInteger, nullable=False)
    source_balance_after: Mapped[int] = mapped_column(type_=BigInteger, nullable=False)
    status: Mapped[TransactionStatus] = mapped_column(SQLEnum(TransactionStatus))
    initiator_type: Mapped[TransactionInitiatorType] = mapped_column(SQLEnum(TransactionInitiatorType), nullable=False)
    description: Mapped[str] = mapped_column()
    destination_id: Mapped[int] = mapped_column(ForeignKey('users.telegram_id'), type_=BigInteger, nullable=True)
    destination: Mapped[User] = relationship("User", foreign_keys=[destination_id])
    source_id: Mapped[int] = mapped_column(ForeignKey('users.telegram_id'), type_=BigInteger, nullable=True)
    source: Mapped[User] = relationship("User", foreign_keys=[source_id])
    created_by_id: Mapped[int] = mapped_column(ForeignKey('users.telegram_id'), type_=BigInteger, nullable=True)
    created_by: Mapped[User] = relationship("User", foreign_keys=[created_by_id])
    created_at = mapped_column("created_at", DateTime, default=now)
    abortedAt = Column(DateTime)
    trace: Mapped[dict] = mapped_column(JSONB, server_default=func.jsonb('{}'))


class Setting(Base):
    __tablename__ = 'settings'

    id: Mapped[SettingsKey] = mapped_column(SQLEnum(SettingsKey), primary_key=True)
    int_val: Mapped[int] = mapped_column(type_=BigInteger, nullable=True)
    str_val: Mapped[str] = mapped_column(nullable=True)


class Mailing(Base):
    __tablename__ = 'mailings'

    id: Mapped[int] = mapped_column(type_=BigInteger, primary_key=True, autoincrement=True)
    files: Mapped[list[str]] = mapped_column(JSONB, server_default=func.jsonb('[]'))
    text: Mapped[str] = mapped_column(type_=Text, nullable=True)
    markup: Mapped[dict] = mapped_column(type_=JSONB, default=None, comment="serialized 'InlineKeyboardMarkup'")
    status: Mapped[MailingStatus] = mapped_column(SQLEnum(MailingStatus))
    created_by_id: Mapped[int] = mapped_column(ForeignKey('users.telegram_id'), type_=BigInteger, nullable=False)
    created_by: Mapped[User] = relationship("User", foreign_keys=[created_by_id])
    created_at = mapped_column("created_at", DateTime, default=now)
    finished_at = mapped_column("finished_at", DateTime, nullable=True)


class MailingMessage(Base):
    __tablename__ = 'mailing_messages'

    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    text: Mapped[str] = mapped_column(type_=Text, nullable=True)
    status: Mapped[MailingMessageStatus] = mapped_column(SQLEnum(MailingMessageStatus))
    destination_id: Mapped[int] = mapped_column(ForeignKey('users.telegram_id'), type_=BigInteger, nullable=False)
    destination: Mapped[User] = relationship("User", foreign_keys=[destination_id])
    mailing_id: Mapped[int] = mapped_column(ForeignKey('mailings.id'), type_=BigInteger, nullable=False)
    mailing: Mapped[Mailing] = relationship("Mailing", foreign_keys=[mailing_id])
    created_at = mapped_column("created_at", DateTime, default=now)
    sent_at = mapped_column(DateTime, nullable=True)
    failed_message: Mapped[str] = mapped_column(type_=Text, nullable=True)


class SlotsBetHistory(Base):
    __tablename__ = 'slots_bet_history'

    id: Mapped[int] = mapped_column(type_=BigInteger, primary_key=True, autoincrement=True)
    bet_amount: Mapped[int] = mapped_column(type_=BigInteger, nullable=False)
    win_amount: Mapped[int] = mapped_column(type_=BigInteger, nullable=True)
    type: Mapped[BetType] = mapped_column(SQLEnum(BetType))
    player_id: Mapped[int] = mapped_column(ForeignKey('users.telegram_id'), type_=BigInteger, nullable=False)
    player: Mapped[User] = relationship("User", foreign_keys=[player_id])
    created_at = mapped_column("created_at", DateTime, default=now)
    trace_uuid: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), default=uuid.uuid4)
