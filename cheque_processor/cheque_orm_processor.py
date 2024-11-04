from sqlalchemy.ext.asyncio import AsyncSession

from cheque import ChequeModifier
from database import ChequeActivation, is_activation_exists, ChequeActivationStatus
from exceptions.cheque import MultipleChequeActivationForbidden


async def new_cheque_activation(cm: ChequeModifier, user_id: int, s: AsyncSession) -> ChequeActivation:
    if await is_activation_exists(cm.entity.id, user_id, cache_id=(cm.entity.id, user_id), s=s):
        raise MultipleChequeActivationForbidden()
    ca = ChequeActivation(
        cheque_id=cm.entity.id,
        user_id=user_id,
        status=ChequeActivationStatus.IN_PROGRESS
    )
    s.add(ca)
    await s.flush()
    return ca
