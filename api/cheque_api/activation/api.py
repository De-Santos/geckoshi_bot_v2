import logging
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from starlette.responses import JSONResponse

import auth
from providers.tg_arg_provider import TgArg
from utils.pagination import PaginatedResponse
from .dto import ChequeActivationDto
from .impl import activate_cheque_impl, get_my_cheque_activations_page_impl, get_cheque_impl, get_cheque_activation_count_impl
from ..dto import ChequeDto

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/activation",
    tags=["cheque-activation"],
)


@router.post(
    '',
    response_model=bool
)
async def activate_cheque(cheque_id: Annotated[int | str, Query(alias='id', description="Id of the cheque")],
                          password: Annotated[str, Query(alias='p', description="Password of the cheque")],
                          encoded: Annotated[bool, Query(alias='e', description="Is the cheque id is encoded")] = False,
                          user_id=Depends(auth.auth_dependency)):
    if encoded:
        cheque_id = TgArg(cheque_id).parse()
    result = await activate_cheque_impl(int(cheque_id), password, user_id)
    return JSONResponse({
        "status": "OK",
        "data": result
    })


@router.get(
    '/cheque-info',
    response_model=ChequeDto
)
async def get_cheque(cheque_id: Annotated[int | str, Query(alias='id', description="Id of the cheque")],
                     encoded: Annotated[bool, Query(alias='e', description="Is the cheque id is encoded")] = False,
                     user_id=Depends(auth.auth_dependency)):
    if encoded:
        cheque_id = TgArg(cheque_id).parse()
    result = await get_cheque_impl(int(cheque_id), user_id)
    return JSONResponse({
        "status": "OK",
        "data": result.model_dump(mode='json')
    })


@router.get(
    '/cheque-info/count',
    response_model=ChequeDto
)
async def get_cheque_activation_count(cheque_id: Annotated[int | str, Query(alias='id', description="Id of the cheque")],
                                      encoded: Annotated[bool, Query(alias='e', description="Is the cheque id is encoded")] = False,
                                      user_id=Depends(auth.auth_dependency)):
    if encoded:
        cheque_id = TgArg(cheque_id).parse()
    result = await get_cheque_activation_count_impl(int(cheque_id), user_id)
    return JSONResponse({
        "status": "OK",
        "data": {
            "count": result,
        }
    })


@router.get(
    '',
    response_model=ChequeActivationDto
)
async def get_my_cheque_activations_page(user_id=Depends(auth.auth_dependency),
                                         page: int = 1,
                                         limit: int = 1):
    result = await get_my_cheque_activations_page_impl(user_id, page, limit)
    return PaginatedResponse(result)
