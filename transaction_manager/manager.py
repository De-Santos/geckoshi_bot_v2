from sqlalchemy import func

from database import TransactionOperation, get_session, Transaction, get_user_by_tg, User, TransactionStatus, TransactionType, TransactionInitiatorType


def __process_operation(balance: int, operation: TransactionOperation, amount: int) -> int:
    if operation == TransactionOperation.OVERRIDE:
        return amount
    elif operation == TransactionOperation.INCREMENT:
        return balance + amount
    elif operation == TransactionOperation.DECREMENT:
        nb = balance - amount
        if nb < 0:
            raise Exception(f"balance can't be negative number")
        return nb


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
        new_destination_user_balance = __process_operation(destination_user.balance, operation, amount)
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


def make_transaction_from_system(target: int, operation: TransactionOperation, amount: int,
                                 transaction_type: TransactionType = TransactionType.INTERNAL,
                                 created_by: int | None = None,
                                 description: str = None):
    session = get_session()
    session.begin()
    user: User = get_user_by_tg(session, target)
    new_balance = __process_operation(user.balance, operation, amount)
    transaction = Transaction(
        operation=operation,
        type=transaction_type,
        amount=amount,
        destination_balance_before=user.balance,
        destination_balance_after=new_balance,
        source_balance_before=0,
        source_balance_after=0,
        status=TransactionStatus.COMPLETED,
        destination_id=user.telegram_id,
        created_by_id=created_by,
        description=description,
        initiator_type=TransactionInitiatorType.SYSTEM
    )
    session.add(transaction)
    user.balance = new_balance
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
