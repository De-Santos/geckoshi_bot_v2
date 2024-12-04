from sqlalchemy.ext.asyncio import AsyncSession

import rabbit
from cheque import ChequeModifier
from cheque_processor.cheque_orm_processor import new_cheque_activation
from database import ChequeType, with_session
from rabbit.classes import ActivationChequeDto, ChequePaybackDto
from rabbit.producers import SingleMessagePublisher


async def activate_cheque(cm: ChequeModifier, user_id: int) -> bool:
    if cm.entity.type == ChequeType.PERSONAL:
        return await __activate_personal_cheque(cm, user_id)
    elif cm.entity.type == ChequeType.MULTY:
        return await __activate_multi_cheque(cm, user_id)
    else:
        raise NotImplementedError()


@with_session(transaction=True)
async def __activate_personal_cheque(cm: ChequeModifier, user_id: int, s: AsyncSession = None) -> bool:
    ca = await new_cheque_activation(cm, user_id, s)

    async with SingleMessagePublisher(queue_name=rabbit.Queue.PERSONAL_CHEQUE_ACTIVATION.value) as publisher:
        result = await publisher.publish(ActivationChequeDto(
            user_id=user_id,
            cheque_id=cm.entity.id,
            cheque_activation_id=ca.id
        ))
    return result


@with_session(transaction=True)
async def __activate_multi_cheque(cm: ChequeModifier, user_id: int, s: AsyncSession = None) -> bool:
    ca = await new_cheque_activation(cm, user_id, s)

    async with SingleMessagePublisher(queue_name=rabbit.Queue.MULTI_CHEQUE_ACTIVATION.value) as publisher:
        result = await publisher.publish(ActivationChequeDto(
            user_id=user_id,
            cheque_id=cm.entity.id,
            cheque_activation_id=ca.id
        ))
    return result


async def order_payback(cm: ChequeModifier) -> bool:
    if cm.entity.deleted_at is None:
        raise RuntimeError()

    async with SingleMessagePublisher(queue_name=rabbit.Queue.CHEQUE_PAYBACK_ORDERS.value) as publisher:
        result = await publisher.publish(ChequePaybackDto(cheque_id=cm.entity.id))
    return result


__all__ = [
    'activate_cheque',
    'order_payback',
]
