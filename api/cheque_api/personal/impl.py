import cheque
import links
from .dto import NewPersonalChequeDto, PersonalChequeDto
from cheque import ChequeModifier
from database import ChequeType, CurrencyType
from providers.tg_arg_provider import ArgType


async def create_new_cheque_impl(dto: NewPersonalChequeDto, user_id: int) -> PersonalChequeDto:
    cm: ChequeModifier = await cheque.generate(
        amount=dto.amount,
        name=dto.name,
        creator_id=user_id,
        type_=ChequeType.PERSONAL,
        currency=CurrencyType.GMEME,
    )

    pcd = PersonalChequeDto.model_validate(cm.entity, from_attributes=True)
    pcd.link = links.simple_generate(ArgType.CHEQUE, cm.entity.id)
    return pcd
