from typing import Optional, Union

import cheque
import links
from chat_processor.member import check_bot_in_chats
from cheque import ChequeModifier, get_active, get_active_page, get_deleted_page
from cheque.methods import get_historic_page
from cheque_processor.manager import order_payback
from database import ChequeType, CurrencyType
from exceptions.cheque import ChequeIsNotModifiable, ChequeModificationForbidden, ChequeForbidden, ChequeInactive, InaccessibleChatInChequeRequirements
from providers.tg_arg_provider import ArgType
from utils.pagination import Pagination
from .dto import NewMultiChequeDto
from ..dto import ChequeDto


def __to_dto(cm: ChequeModifier) -> ChequeDto:
    pcd = ChequeDto.model_validate(cm.entity, from_attributes=True)
    pcd.link = links.simple_generate(ArgType.CHEQUE, cm.entity.id)
    return pcd


async def check_access_to_the_chats(chat_ids: list[Union[int, str]] | None) -> None:
    if chat_ids is None or len(chat_ids) == 0:
        return
    if not check_bot_in_chats(chat_ids):
        raise InaccessibleChatInChequeRequirements()


async def create_new_cheque_impl(dto: NewMultiChequeDto, user_id: int) -> ChequeDto:
    await check_access_to_the_chats(dto.require_subscriptions)
    cm: ChequeModifier = await cheque.generate(
        amount=dto.amount,
        name=dto.name,
        creator_id=user_id,
        type_=ChequeType.MULTY,
        currency=CurrencyType.GMEME,
        description=dto.description,
        activation_limit=dto.activation_limit,
        password=dto.password,
        require_subscriptions=dto.require_subscriptions,
    )

    return __to_dto(cm)


async def update_cheque_impl(dto: ChequeDto, user_id: int) -> ChequeDto:
    cm: Optional[ChequeModifier] = await get_active(dto.id)
    if cm is None:
        raise ChequeIsNotModifiable()
    elif not cm.is_creator(user_id):
        raise ChequeModificationForbidden()

    await cm.update(name=dto.name, description=dto.description, password=dto.password)

    return __to_dto(cm)


async def get_cheque_impl(cheque_id: int) -> ChequeDto:
    cm: Optional[ChequeModifier] = await get_active(cheque_id)

    if cm is None:
        raise ChequeInactive()

    return __to_dto(cm)


async def get_my_cheque_page_impl(user_id: int, page: int = 1, limit: int = 1) -> Pagination[dict]:
    cm_page: Pagination = await get_active_page(user_id, ChequeType.MULTY, page, limit)
    cm_page.map_each(__to_dto)
    cm_page.map_each(lambda dto: dto.model_dump(mode='json'))
    return cm_page


async def get_my_historic_cheque_page_impl(user_id: int, page: int = 1, limit: int = 1) -> Pagination[dict]:
    cm_page: Pagination = await get_historic_page(user_id, ChequeType.MULTY, page, limit)
    cm_page.map_each(__to_dto)
    cm_page.map_each(lambda dto: dto.model_dump(mode='json'))
    return cm_page


async def get_my_deleted_cheque_page_impl(user_id: int, page: int = 1, limit: int = 1) -> Pagination[dict]:
    cm_page: Pagination = await get_deleted_page(user_id, ChequeType.MULTY, page, limit)
    cm_page.map_each(__to_dto)
    cm_page.map_each(lambda dto: dto.model_dump(mode='json'))
    return cm_page


async def delete_cheque_impl(cheque_id: int, user_id: int) -> bool:
    cm: Optional[ChequeModifier] = await get_active(cheque_id)

    if cm.entity.type != ChequeType.MULTY:
        raise ChequeForbidden()
    if cm is None:
        raise ChequeInactive()
    elif not (cm.is_creator(user_id)):
        raise ChequeForbidden()

    await cm.delete_cheque(initiator=user_id)
    return await order_payback(cm)
