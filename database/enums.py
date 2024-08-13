from enum import Enum


class TransactionOperation(Enum):
    INCREMENT = 0
    DECREMENT = 1
    OVERRIDE = 2


class TransactionType(Enum):
    INTERNAL = 0
    WITHDRAW = 1


class TransactionStatus(Enum):
    PENDING = 0
    COMPLETED = 1
    FAILED = 2
    ABORTED = 3


class TransactionInitiatorType(Enum):
    SYSTEM = 0
    ADMIN = 1
    USER = 2


class SettingsKey(Enum):
    PAY_FOR_REFERRAL = 1
    MIN_WITHDRAW_IN_AIRDROP = 2
    PREMIUM_GMEME_PRICE = 3


class MailingStatus(Enum):
    IN_PROGRESS = 0
    COMPLETED = 1
    CANCELED = 2


class MailingMessageStatus(Enum):
    IN_PROGRESS = 0
    IN_QUEUE = 1
    COMPLETED = 2
    FAILED = 3
    CANCELED = 4
