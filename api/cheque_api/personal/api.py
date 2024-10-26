import logging
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from starlette.responses import JSONResponse

import auth
from utils.pagination import PaginatedResponse
from .dto import NewPersonalChequeDto, PersonalChequeDto
from .impl import create_new_cheque_impl, update_cheque_impl, get_cheque_impl, get_my_cheque_page_impl, get_my_historic_cheque_page_impl

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/personal",
    tags=["cheque-personal"],
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


@router.get(
    '',
    response_model=PersonalChequeDto
)
async def get_cheque(cheque_id: Annotated[int, Query(alias='id', description="Id of the cheque")],
                     user_id=Depends(auth.auth_dependency)):
    result = await get_cheque_impl(cheque_id, user_id)
    return JSONResponse({
        "status": "OK",
        "data": result.model_dump(mode='json')
    })


@router.get(
    '/my',
    response_model=PersonalChequeDto
)
async def get_my_cheque_page(user_id=Depends(auth.auth_dependency),
                             page: int = 1,
                             limit: int = 1):
    result = await get_my_cheque_page_impl(user_id, page, limit)
    return PaginatedResponse(result)


@router.get(
    '/my/historic',
    response_model=PersonalChequeDto
)
async def get_my_historic_cheque_page(user_id=Depends(auth.auth_dependency),
                                      page: int = 1,
                                      limit: int = 1):
    result = await get_my_historic_cheque_page_impl(user_id, page, limit)
    return PaginatedResponse(result)
