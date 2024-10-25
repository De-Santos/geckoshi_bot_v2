import logging

from fastapi import APIRouter, Depends
from starlette.responses import JSONResponse

import auth
from .dto import NewPersonalChequeDto, PersonalChequeDto
from .impl import create_new_cheque_impl, update_cheque_impl

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/personal",
    tags=["cheque"],
)


@router.post(
    '',
    response_model=PersonalChequeDto
)
async def create_new_cheque(dto: NewPersonalChequeDto,
                            user_id=Depends(auth.auth_dependency)):
    result = await create_new_cheque_impl(dto, user_id)
    return JSONResponse({
        "status": "OK",
        "data": result.model_dump(mode='json')
    })


@router.patch(
    '',
    response_model=PersonalChequeDto
)
async def update_cheque(dto: PersonalChequeDto,
                        user_id=Depends(auth.auth_dependency)):
    result = await update_cheque_impl(dto, user_id)
    return JSONResponse({
        "status": "OK",
        "data": result.model_dump(mode='json')
    })
