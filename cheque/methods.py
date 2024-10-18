from typing import Optional
from uuid import uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from database import CurrencyType, with_session, Cheque, ChequeType, TransactionOperation, get_active_cheque_by_id
from transaction_manager import make_transaction_from_system, generate_trace, TraceType
from .classes import ChequeModifier


@with_session
async def generate(
        amount: int,
        creator_id: int,
        type_: ChequeType,
        currency: CurrencyType,
        s: AsyncSession = None,
) -> ChequeModifier:
    trace_uid = uuid4()

    await make_transaction_from_system(
        target=creator_id,
        operation=TransactionOperation.DECREMENT,
        amount=amount,
        created_by=creator_id,
        description='cheque amount allocation',
        trace=generate_trace(TraceType.CHEQUE, str(trace_uid)),
        session=s,
        currency_type=currency,
        auto_commited=False
    )

    entity = Cheque(
        type=type_,
        amount=amount,
        currency_type=currency,
        created_by_id=creator_id,
        trace_uuid=trace_uid
    )
    s.add(entity)
    await s.commit()
    return ChequeModifier(entity=entity)


async def get_active(id_: int) -> Optional[ChequeModifier]:
    cheque: Optional[Cheque] = await get_active_cheque_by_id(id_)
    if cheque is None:
        return None
    return ChequeModifier(entity=cheque)


__all__ = [
    'generate',
    'get_active',
]
