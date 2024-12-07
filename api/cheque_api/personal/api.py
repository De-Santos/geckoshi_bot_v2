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
    response_model=ChequeDto,
    summary="Create a New Personal Cheque",
    description="""
Creates a new personal cheque for the authenticated user. 
The cheque details must be provided in the request body. The cheque will be linked to the authenticated user.
"""
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
    response_model=ChequeDto,
    summary="Update an Existing Personal Cheque",
    description="""
Updates the details of an existing cheque belonging to the authenticated user.
The updated cheque details must be included in the request body.
"""
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
    response_model=ChequeDto,
    summary="Retrieve Paginated List of My Personal Cheques",
    description="""
Retrieves a paginated list of active personal cheques associated with the authenticated user.
Use query parameters `page` and `limit` to control pagination.
"""
)
async def get_my_cheque_page(user_id=Depends(auth.auth_dependency),
                             page: int = 1,
                             limit: int = 1):
    result = await get_my_cheque_page_impl(user_id, page, limit)
    return PaginatedResponse(result)


@router.get(
    '/my/historic',
    response_model=ChequeDto,
    summary="Retrieve Paginated List of My Personal Historic Cheques",
    description="""
Retrieves a paginated list of historic (completed) personal cheques associated with the authenticated user.
Use query parameters `page` and `limit` to control pagination.
"""
)
async def get_my_historic_cheque_page(user_id=Depends(auth.auth_dependency),
                                      page: int = 1,
                                      limit: int = 1):
    result = await get_my_historic_cheque_page_impl(user_id, page, limit)
    return PaginatedResponse(result)


@router.delete(
    '',
    summary="Delete a Personal Cheque",
    description="""
Deletes a specific cheque belonging to the authenticated user.
The cheque ID must be provided as a query parameter.
"""
)
async def delete_cheque(cheque_id: Annotated[int, Query(alias='id', description="Unique identifier of the cheque")],
                        user_id=Depends(auth.auth_dependency)):
    result: bool = await delete_cheque_impl(cheque_id, user_id)
    return JSONResponse({"status": "OK",
                         "result": result})


@router.get(
    '/my/deleted',
    response_model=ChequeDto,
    summary="Retrieve Paginated List of My Deleted Personal Cheques",
    description="""
Retrieves a paginated list of deleted personal cheques associated with the authenticated user.
Use query parameters `page` and `limit` to control pagination.
"""
)
async def get_my_deleted_cheques(user_id=Depends(auth.auth_dependency),
                                 page: int = 1,
                                 limit: int = 1):
    result = await get_my_deleted_cheque_page_impl(user_id, page, limit)
    return PaginatedResponse(result)
