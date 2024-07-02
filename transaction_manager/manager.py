from database import TransactionOperation, get_session, Transaction, get_user_by_tg, User, TransactionStatus


def __process_operation(balance: int, operation: TransactionOperation, amount: int) -> int:
    if operation == TransactionOperation.OVERRIDE:
        return amount
    elif operation == TransactionOperation.INCREMENT:
        return balance + amount
    elif operation == TransactionOperation.DECREMENT:
        return balance - amount


def make_transaction(tg_user_id: int, created_by: int, operation: TransactionOperation, amount: int,
                     description: str = None):
    session = get_session()
    session.begin()
    user: User = get_user_by_tg(session, tg_user_id)
    new_balance = __process_operation(user.balance, operation, amount)
    transaction = Transaction(
        operation=operation,
        amount=amount,
        balance_before=user.balance,
        balance_after=new_balance,
        status=TransactionStatus.COMPLETED,
        destination_id=tg_user_id,
        created_by_id=created_by,
        description=description
    )
    session.add(transaction)
    user.balance = new_balance
    session.commit()
