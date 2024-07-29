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


class SettingsKey(Enum):
    PAY_FOR_REFERRAL = 1
    MIN_WITHDRAW_IN_AIRDROP = 2
