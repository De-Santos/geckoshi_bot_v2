from typing import Optional

import cheque_processor
import links
from cheque import ChequeModifier, get_active
from database import get_cheque_activation_page, ChequeActivation, Cheque, ChequeType
from exceptions.cheque import ChequeInactive, ChequeForbidden
from providers.tg_arg_provider import ArgType
from utils.pagination import Pagination
from .dto import ChequeActivationDto
from ..dto import ChequeDto


def __cheque_to_dto(c: Cheque) -> ChequeDto:
    cd = ChequeDto.model_validate(c, from_attributes=True)
    cd.link = links.simple_generate(ArgType.CHEQUE, c.id)
    return cd


def __activation_to_dto(activation: ChequeActivation) -> ChequeActivationDto:
    cad = ChequeActivationDto.model_validate(activation, from_attributes=True)
    cad.cheque_info = __cheque_to_dto(activation.cheque)
    return cad


async def activate_cheque_impl(cheque_id: int, user_id: int) -> bool:
    cm: Optional[ChequeModifier] = await get_active(cheque_id)
    if cm is None:
        raise ChequeInactive()

    return await cheque_processor.activate_cheque(cm, user_id)


async def get_my_cheque_activations_page_impl(user_id: int, page: int = 1, limit: int = 1) -> Pagination[dict]:
    a_page: Pagination = await get_cheque_activation_page(user_id, page, limit)
    a_page.map_each(__activation_to_dto)
    a_page.map_each(lambda dto: dto.model_dump(mode='json'))
    return a_page


async def get_cheque_impl(cheque_id: int, user_id: int) -> ChequeDto:
    cm: Optional[ChequeModifier] = await get_active(cheque_id)

    if cm is None:
        raise ChequeInactive()
    elif cm.entity.type == ChequeType.PERSONAL:
        if not (cm.is_creator(user_id) or cm.is_connected_to_user(user_id)):
            raise ChequeForbidden()

    return __cheque_to_dto(cm.entity)
