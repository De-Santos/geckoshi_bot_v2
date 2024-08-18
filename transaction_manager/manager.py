from typing import Tuple

from sqlalchemy import func
from sqlalchemy.orm import Session

from database import TransactionOperation, get_session, Transaction, get_user_by_tg, User, TransactionStatus, TransactionType, TransactionInitiatorType, CurrencyType


def __calculate_operation(balance: int, operation: TransactionOperation, amount: int) -> int:
    if operation == TransactionOperation.OVERRIDE:
        return amount
    elif operation == TransactionOperation.INCREMENT:
        return balance + amount
    elif operation == TransactionOperation.DECREMENT:
        nb = balance - amount
        if nb < 0:
            raise Exception("balance can't be negative number")
        return nb


def __process_operation(balance: int, *args) -> Tuple[int, int]:
    return balance, __calculate_operation(balance, *args)


def __currency_based_operation(user: User, operation: TransactionOperation,
                               currency_type: CurrencyType, amount: int) -> Tuple[int, int]:
    if currency_type == CurrencyType.GMEME:
        old, new = __process_operation(user.balance, operation, amount)
        user.balance = new
        return old, new
    elif currency_type == CurrencyType.BMEME:
        old, new = __process_operation(user.bmeme_balance, operation, amount)
        user.bmeme_balance = new
        return old, new
    else:
        raise Exception(f"Unhandled currency type: {currency_type}")


def make_transaction(destination: int | None, source_user_id: int | None, created_by: int, operation: TransactionOperation, amount: int,
                     transaction_type: TransactionType = TransactionType.INTERNAL,
                     description: str = None):
    session = get_session()
    session.begin()
    destination_balance_before = 0
    new_destination_user_balance = 0
    if destination is not None:
        destination_user: User = get_user_by_tg(session, destination)
        destination_balance_before = destination_user.balance
        new_destination_user_balance = __calculate_operation(destination_user.balance, operation, amount)
    source_user: User = get_user_by_tg(session, source_user_id)
    transaction = Transaction(
        operation=operation,
        type=transaction_type,
        amount=amount,
        destination_balance_before=destination_balance_before,
        destination_balance_after=new_destination_user_balance,
        status=TransactionStatus.COMPLETED,
        destination_id=destination,
        source_id=source_user_id,
        created_by_id=created_by,
        description=description
    )
    session.add(transaction)
    destination_user.balance = new_destination_user_balance
    session.commit()


def make_transaction_from_system(target: int,
                                 operation: TransactionOperation,
                                 amount: int,
                                 transaction_type: TransactionType = TransactionType.INTERNAL,
                                 created_by: int | None = None,
                                 description: str = None,
                                 trace: dict = None,
                                 session: Session = None,
                                 currency_type: CurrencyType = CurrencyType.GMEME):
    if session is None:
        session = get_session()
        session.begin()
    user: User = get_user_by_tg(session, target)
    old, new = __currency_based_operation(user, operation, currency_type, amount)
    transaction = Transaction(
        operation=operation,
        type=transaction_type,
        amount=amount,
        currency_type=currency_type,
        destination_balance_before=old,
        destination_balance_after=new,
        source_balance_before=0,
        source_balance_after=0,
        status=TransactionStatus.COMPLETED,
        destination_id=user.telegram_id,
        created_by_id=created_by,
        description=description,
        initiator_type=TransactionInitiatorType.SYSTEM,
        trace=trace
    )
    session.add(transaction)
    session.commit()


def select_transactions_sum_amount(tg_user_id: int, transaction_type: TransactionType) -> int:
    s = get_session()
    stmt = (s.query(func.sum(Transaction.amount))
            .where(Transaction.source_id.__eq__(tg_user_id))
            .where(Transaction.type.__eq__(transaction_type)))
    result = stmt.scalar()
    if result is None:
        return 0
    return result
