from typing import Optional

import cheque
import links
from cheque import ChequeModifier, get_active
from database import ChequeType, CurrencyType
from exceptions.cheque import ChequeIsNotModifiable, ChequeModificationForbidden
from providers.tg_arg_provider import ArgType
from .dto import NewPersonalChequeDto, PersonalChequeDto


async def create_new_cheque_impl(dto: NewPersonalChequeDto, user_id: int) -> PersonalChequeDto:
    cm: ChequeModifier = await cheque.generate(
        amount=dto.amount,
        name=dto.name,
        creator_id=user_id,
        type_=ChequeType.PERSONAL,
        currency=CurrencyType.GMEME,
        description=dto.description,
    )

    pcd = PersonalChequeDto.model_validate(cm.entity, from_attributes=True)
    pcd.link = links.simple_generate(ArgType.CHEQUE, cm.entity.id)
    return pcd


async def update_cheque_impl(dto: PersonalChequeDto, user_id: int) -> PersonalChequeDto:
    cm: Optional[ChequeModifier] = await get_active(dto.id)
    if cm is None:
        raise ChequeIsNotModifiable()
    elif not cm.is_creator(user_id):
        raise ChequeModificationForbidden()

    await cm.update_cheque(name=dto.name, connected_to_user=dto.connected_to_user, description=dto.description)

    pcd = PersonalChequeDto.model_validate(cm.entity, from_attributes=True)
    pcd.link = links.simple_generate(ArgType.CHEQUE, cm.entity.id)
    return pcd
