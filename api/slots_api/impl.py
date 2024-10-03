import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from database import with_session, get_user_balance, SlotsBetHistory, TransactionOperation, BetType
from slots import play_slots
from transaction_manager import make_transaction_from_system, generate_trace, TraceType
from .dto import BetResultDto


@with_session(transaction=True)
async def process_play(user_id: int, amount: int, s: AsyncSession = None) -> BetResultDto:
    balance = await get_user_balance(user_id, s=s)
    if balance < amount:
        raise Exception('Not enough balance')
    trace = uuid.uuid4()
    combination, win_amount, bet_type = play_slots(amount)

    operation = TransactionOperation.INCREMENT if bet_type == BetType.WIN else TransactionOperation.DECREMENT
    amount = win_amount if bet_type == BetType.WIN else amount
    s.add(SlotsBetHistory(bet_amount=amount, win_amount=win_amount, type=bet_type, player_id=user_id, trace_uuid=trace))
    await make_transaction_from_system(user_id, operation, amount, description="slots play", trace=generate_trace(TraceType.SLOTS_BET, str(trace)), session=s)
    return BetResultDto(combination=combination, win_amount=win_amount, bet_type=bet_type)
