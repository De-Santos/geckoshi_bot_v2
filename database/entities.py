import datetime
import uuid
from decimal import Decimal
from typing import Optional

from sqlalchemy import Column, DateTime, ForeignKey, BigInteger, Enum as SQLEnum, Text, func, PrimaryKeyConstraint, Index, CheckConstraint, text, Numeric
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base
from database.enums import CustomClientTokenType
from database.enums import TransactionOperation, TransactionStatus, SettingsKey, TransactionType, TransactionInitiatorType, MailingStatus, MailingMessageStatus, BetType, TaskType, CurrencyType, ChequeType
from database.json_classes import BotApiConfig, UserActivityContext
from database.type_decorators import JSONEncoded, JSONEncodedList
from lang.lang_based_provider import Lang


def now(native: bool = False) -> datetime.datetime:
    dt = datetime.datetime.now(datetime.UTC)
    if native:
        return dt.replace(tzinfo=None)
    return dt


class User(Base):
    __tablename__ = 'users'

    telegram_id: Mapped[int] = mapped_column(type_=BigInteger, primary_key=True)
    balance: Mapped[Decimal] = mapped_column(type_=Numeric(precision=20, scale=8), default=Decimal(0))
    bmeme_balance: Mapped[Decimal] = mapped_column(type_=Numeric(precision=20, scale=8), default=Decimal(0))
    referred_by_id: Mapped[Optional[int]] = mapped_column(ForeignKey('users.telegram_id'), type_=BigInteger)
    blocked: Mapped[bool] = mapped_column(default=False)
    language: Mapped[Lang] = mapped_column(SQLEnum(Lang), default=Lang.EN)
    is_admin: Mapped[bool] = mapped_column(default=False, nullable=False)
    is_premium: Mapped[bool] = mapped_column(default=False, nullable=False)
    created_at = mapped_column("created_at", DateTime(timezone=True), default=now, index=True)
    deleted_at = Column(DateTime(timezone=True), default=None)


class Transaction(Base):
    __tablename__ = 'transactions'

    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    operation: Mapped[TransactionOperation] = mapped_column(SQLEnum(TransactionOperation), nullable=False)
    type: Mapped[TransactionType] = mapped_column(SQLEnum(TransactionType), nullable=False)
    amount: Mapped[Decimal] = mapped_column(type_=Numeric(precision=20, scale=8))
    currency_type: Mapped[CurrencyType] = mapped_column(SQLEnum(CurrencyType), nullable=False)
    destination_balance_before: Mapped[Decimal] = mapped_column(type_=Numeric(precision=20, scale=8), nullable=False)
    destination_balance_after: Mapped[Decimal] = mapped_column(type_=Numeric(precision=20, scale=8), nullable=False)
    source_balance_before: Mapped[Decimal] = mapped_column(type_=Numeric(precision=20, scale=8), nullable=False)
    source_balance_after: Mapped[Decimal] = mapped_column(type_=Numeric(precision=20, scale=8), nullable=False)
    status: Mapped[TransactionStatus] = mapped_column(SQLEnum(TransactionStatus))
    initiator_type: Mapped[TransactionInitiatorType] = mapped_column(SQLEnum(TransactionInitiatorType), nullable=False)
    description: Mapped[str] = mapped_column()
    destination_id: Mapped[int] = mapped_column(ForeignKey('users.telegram_id'), type_=BigInteger, nullable=True)
    destination: Mapped[User] = relationship("User", foreign_keys=[destination_id])
    source_id: Mapped[int] = mapped_column(ForeignKey('users.telegram_id'), type_=BigInteger, nullable=True)
    source: Mapped[User] = relationship("User", foreign_keys=[source_id])
    created_by_id: Mapped[int] = mapped_column(ForeignKey('users.telegram_id'), type_=BigInteger, nullable=True)
    created_by: Mapped[User] = relationship("User", foreign_keys=[created_by_id])
    created_at = mapped_column("created_at", DateTime(timezone=True), default=now)
    abortedAt = Column(DateTime(timezone=True))
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
    created_at: Mapped[datetime.datetime] = mapped_column("created_at", DateTime(timezone=True), default=now)
    finished_at: Mapped[datetime.datetime] = mapped_column("finished_at", DateTime(timezone=True), nullable=True)


class MailingMessage(Base):
    __tablename__ = 'mailing_messages'

    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    text: Mapped[str] = mapped_column(type_=Text, nullable=True)
    status: Mapped[MailingMessageStatus] = mapped_column(SQLEnum(MailingMessageStatus))
    destination_id: Mapped[int] = mapped_column(ForeignKey('users.telegram_id'), type_=BigInteger, nullable=False)
    destination: Mapped[User] = relationship("User", foreign_keys=[destination_id])
    mailing_id: Mapped[int] = mapped_column(ForeignKey('mailings.id'), type_=BigInteger, nullable=False)
    mailing: Mapped[Mailing] = relationship("Mailing", foreign_keys=[mailing_id], lazy='joined')
    created_at: Mapped[datetime.datetime] = mapped_column("created_at", DateTime(timezone=True), default=now)
    sent_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    failed_message: Mapped[str] = mapped_column(type_=Text, nullable=True)


class SlotsBetHistory(Base):
    __tablename__ = 'slots_bet_history'

    id: Mapped[int] = mapped_column(type_=BigInteger, primary_key=True, autoincrement=True)
    bet_amount: Mapped[int] = mapped_column(type_=BigInteger, nullable=False)
    win_amount: Mapped[int] = mapped_column(type_=BigInteger, nullable=True)
    type: Mapped[BetType] = mapped_column(SQLEnum(BetType))
    player_id: Mapped[int] = mapped_column(ForeignKey('users.telegram_id'), type_=BigInteger, nullable=False)
    player: Mapped[User] = relationship("User", foreign_keys=[player_id])
    created_at: Mapped[datetime.datetime] = mapped_column("created_at", DateTime(timezone=True), default=now)
    trace_uuid: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), default=uuid.uuid4)


class Task(Base):
    __tablename__ = 'tasks'

    id: Mapped[int] = mapped_column(type_=BigInteger, primary_key=True, autoincrement=True)

    type: Mapped[TaskType] = mapped_column(SQLEnum(TaskType))
    title: Mapped[str] = mapped_column(type_=Text, nullable=True)
    text: Mapped[str] = mapped_column(type_=Text, nullable=True)
    markup: Mapped[dict] = mapped_column(type_=JSONB, default=None, comment="serialized 'InlineKeyboardMarkup'")
    require_subscriptions: Mapped[list] = mapped_column(type_=JSONB, server_default=func.jsonb('[]'))

    api_configs: Mapped[list[BotApiConfig]] = mapped_column(type_=JSONEncodedList(BotApiConfig), nullable=False, server_default=func.jsonb('[]'), comment="Stores API configurations for interactions with other projects")

    coin_type: Mapped[CurrencyType] = mapped_column(SQLEnum(CurrencyType), nullable=False)

    done_limit: Mapped[int] = mapped_column(type_=BigInteger, nullable=True)
    coin_pool: Mapped[int] = mapped_column(type_=BigInteger, nullable=True)
    done_reward: Mapped[int] = mapped_column(type_=BigInteger, nullable=True)

    created_by_id: Mapped[int] = mapped_column(ForeignKey('users.telegram_id'), type_=BigInteger, nullable=False)
    created_by: Mapped[User] = relationship("User", foreign_keys=[created_by_id])

    created_at: Mapped[datetime.datetime] = mapped_column("created_at", DateTime(timezone=True), default=now)
    expires_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), nullable=True)

    deleted_by_id: Mapped[int] = mapped_column(ForeignKey('users.telegram_id'), type_=BigInteger, nullable=True)
    deleted_by: Mapped[User] = relationship("User", foreign_keys=[deleted_by_id])
    deleted_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), nullable=True)

    trace_uuid: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), default=uuid.uuid4)


class TaskDoneHistory(Base):
    __tablename__ = 'tasks_done_history'

    id: Mapped[int] = mapped_column(type_=BigInteger, primary_key=True, autoincrement=True)
    reward: Mapped[int] = mapped_column(type_=BigInteger, nullable=True)

    user_id: Mapped[int] = mapped_column(ForeignKey('users.telegram_id'), type_=BigInteger, nullable=False)
    user: Mapped[User] = relationship("User", foreign_keys=[user_id])

    task_id: Mapped[int] = mapped_column(ForeignKey('tasks.id'), type_=BigInteger, nullable=False)
    task: Mapped[Mailing] = relationship("Task", foreign_keys=[task_id])
    created_at: Mapped[datetime.datetime] = mapped_column("created_at", DateTime(timezone=True), default=now)


class UserActivityStatistic(Base):
    __tablename__ = 'user_activity_statistics'

    __table_args__ = (
        PrimaryKeyConstraint('user_id', 'datetime', name='user_activity_statistics_pk'),
    )

    user_id: Mapped[int] = mapped_column(ForeignKey('users.telegram_id'), type_=BigInteger, nullable=False)
    context: Mapped[UserActivityContext] = mapped_column(type_=JSONEncoded(UserActivityContext), server_default=func.jsonb('{}'))
    datetime_: Mapped[datetime.datetime] = mapped_column("datetime", DateTime(timezone=True), default=now)


class CustomClientToken(Base):
    __tablename__ = 'custom_client_tokens'

    id: Mapped[str] = mapped_column(type_=Text, primary_key=True)
    name: Mapped[str] = mapped_column(type_=Text, nullable=True)
    type: Mapped[CustomClientTokenType] = mapped_column(SQLEnum(CustomClientTokenType), nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column("created_at", DateTime(timezone=True), default=now)
    deleted_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), nullable=True)


class EventBonus(Base):
    __tablename__ = 'event_bonuses'
    id: Mapped[int] = mapped_column(type_=BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(type_=Text, nullable=True)
    cooldown: Mapped[str] = mapped_column(nullable=False)
    conversion_to: Mapped[CurrencyType] = mapped_column(SQLEnum(CurrencyType), nullable=False)
    min_win: Mapped[int] = mapped_column(type_=BigInteger, nullable=False)
    max_win: Mapped[int] = mapped_column(type_=BigInteger, nullable=False)
    start_datetime: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    end_datetime: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class EventBonusActivation(Base):
    __tablename__ = 'event_bonus_activations'

    __table_args__ = (
        PrimaryKeyConstraint('user_id', 'datetime', name='event_bonus_activations_pk'),
        Index('ix_user_event_bonus', 'user_id', 'event_bonus_id'),
    )

    user_id: Mapped[int] = mapped_column(ForeignKey('users.telegram_id'), type_=BigInteger, nullable=False)
    datetime_: Mapped[datetime.datetime] = mapped_column("datetime", DateTime(timezone=True), default=now)
    amount: Mapped[int] = mapped_column(type_=BigInteger, nullable=False)
    event_bonus_id: Mapped[int] = mapped_column(ForeignKey('event_bonuses.id'), type_=BigInteger, nullable=False)


class Cheque(Base):
    __tablename__ = 'cheques'

    __table_args__ = (
        CheckConstraint('connected_to_user != created_by_id', name='check_connected_user_not_created_by'),
    )

    id: Mapped[int] = mapped_column(type_=BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(type_=Text, nullable=True, default=lambda: f"cheque-{str(uuid.uuid4())[:5]}")
    type: Mapped[ChequeType] = mapped_column(SQLEnum(ChequeType), nullable=False)
    amount: Mapped[Decimal] = mapped_column(type_=Numeric(precision=20, scale=8), nullable=False)
    currency_type: Mapped[CurrencyType] = mapped_column(SQLEnum(CurrencyType), nullable=False)
    description: Mapped[str] = mapped_column(type_=Text, nullable=True)
    connected_to_user: Mapped[int] = mapped_column(type_=BigInteger, nullable=True)
    activation_limit: Mapped[int] = mapped_column(type_=BigInteger, nullable=False, server_default=text('1'))

    created_by_id: Mapped[int] = mapped_column(ForeignKey('users.telegram_id'), type_=BigInteger, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column("created_at", DateTime(timezone=True), default=now, nullable=False)
    deleted_by_id: Mapped[int] = mapped_column(ForeignKey('users.telegram_id'), type_=BigInteger, nullable=True)
    deleted_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), nullable=True)

    allocation_transaction_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey('transactions.id'), type_=PG_UUID, nullable=False)
    trace_uuid: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), default=uuid.uuid4, nullable=False)


class ChequeActivation(Base):
    __tablename__ = 'cheque_activations'

    id: Mapped[int] = mapped_column(type_=BigInteger, primary_key=True, autoincrement=True)
    cheque_id: Mapped[int] = mapped_column(ForeignKey('cheques.id'), type_=BigInteger, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.telegram_id'), type_=BigInteger, nullable=False)
    datetime_: Mapped[datetime.datetime] = mapped_column("datetime", DateTime(timezone=True), default=now)
    trace_uuid: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), default=uuid.uuid4, nullable=False)
