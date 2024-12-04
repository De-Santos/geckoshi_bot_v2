import logging
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from starlette.responses import JSONResponse

import auth
from utils.pagination import PaginatedResponse
from .dto import NewPersonalChequeDto
from .impl import create_new_cheque_impl, update_cheque_impl, get_my_cheque_page_impl, get_my_historic_cheque_page_impl, delete_cheque_impl, get_my_deleted_cheque_page_impl
from ..dto import ChequeDto

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/personal",
    tags=["cheque-personal"],
)


@router.post(
    '',
    response_model=ChequeDto
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
    response_model=ChequeDto
)
async def update_cheque(dto: ChequeDto,
                        user_id=Depends(auth.auth_dependency)):
    result = await update_cheque_impl(dto, user_id)
    return JSONResponse({
        "status": "OK",
        "data": result.model_dump(mode='json')
    })


@router.get(
    '/my',
    response_model=ChequeDto
)
async def get_my_cheque_page(user_id=Depends(auth.auth_dependency),
                             page: int = 1,
                             limit: int = 1):
    result = await get_my_cheque_page_impl(user_id, page, limit)
    return PaginatedResponse(result)


@router.get(
    '/my/historic',
    response_model=ChequeDto
)
async def get_my_historic_cheque_page(user_id=Depends(auth.auth_dependency),
                                      page: int = 1,
                                      limit: int = 1):
    result = await get_my_historic_cheque_page_impl(user_id, page, limit)
    return PaginatedResponse(result)


@router.delete('')
async def delete_cheque(cheque_id: Annotated[int, Query(alias='id', description="Id of the cheque")],
                        user_id=Depends(auth.auth_dependency)):
    result: bool = await delete_cheque_impl(cheque_id, user_id)
    return JSONResponse({"status": "OK",
                         "result": result})


@router.get(
    '/my/deleted',
    response_model=ChequeDto
)
async def get_my_deleted_cheques(user_id=Depends(auth.auth_dependency),
                                 page: int = 1,
                                 limit: int = 1):
    result = await get_my_deleted_cheque_page_impl(user_id, page, limit)
    return PaginatedResponse(result)
