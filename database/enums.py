from enum import Enum


class TransactionOperation(Enum):
    INCREMENT = 0
    DECREMENT = 1
    OVERRIDE = 2


class TransactionStatus(Enum):
    PENDING = 0
    COMPLETED = 1
    FAILED = 2
    ABORTED = 3
