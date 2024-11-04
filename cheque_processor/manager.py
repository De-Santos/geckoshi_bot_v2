from sqlalchemy.ext.asyncio import AsyncSession

import rabbit
from cheque import ChequeModifier
from cheque_processor.cheque_orm_processor import new_cheque_activation
from database import ChequeType, with_session
from rabbit.classes import ActivationPersonalChequeDto
from rabbit.producers import SingleMessagePublisher


async def activate_cheque(cm: ChequeModifier, user_id: int) -> bool:
    if cm.entity.type == ChequeType.PERSONAL:
        return await __activate_personal_cheque(cm, user_id)
    else:
        raise NotImplementedError()


@with_session(transaction=True)
async def __activate_personal_cheque(cm: ChequeModifier, user_id: int, s: AsyncSession = None) -> bool:
    ca = await new_cheque_activation(cm, user_id, s)

    async with SingleMessagePublisher(queue_name=rabbit.Queue.PERSONAL_CHEQUE_ACTIVATION.value) as publisher:
        result = await publisher.publish(ActivationPersonalChequeDto(
            user_id=user_id,
            cheque_id=cm.entity.id,
            cheque_activation_id=ca.id
        ))
    return result


__all__ = [
    'activate_cheque'
]
