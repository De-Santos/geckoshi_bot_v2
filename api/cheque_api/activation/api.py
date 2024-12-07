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
    response_model=bool,
    summary="Activate a Cheque",
    description="""
Activates a cheque for the authenticated user. The cheque ID, its password, and whether the ID is encoded 
must be provided as query parameters. This process initiates the activation workflow.

Activation workflow:
1. Initiate the activation.
2. Add the activation to the queue.
3. Receive the activation in the queue consumer.
4. Validate the conditions.
5. Complete the activation process.
"""
)
async def activate_cheque(cheque_id: Annotated[int | str, Query(alias='id', description="Unique identifier of the cheque")],
                          password: Annotated[str, Query(alias='p', description="Password of the cheque")],
                          encoded: Annotated[bool, Query(alias='e', description="Indicates whether the cheque ID is encoded")] = False,
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
    response_model=ChequeDto,
    summary="Retrieve Cheque Details",
    description="""
Retrieves the details of a specific cheque. 
Provide the cheque ID as a query parameter, and optionally indicate whether the ID is encoded.
"""
)
async def get_cheque(cheque_id: Annotated[int | str, Query(alias='id', description="Unique identifier of the cheque")],
                     encoded: Annotated[bool, Query(alias='e', description="Indicates whether the cheque ID is encoded")] = False,
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
    response_model=ChequeDto,
    summary="Get Activation Count of a Cheque",
    description="""
Retrieves the total number of successful activations for a specific cheque. The cheque must belong to the authenticated user.
Provide the cheque ID as a query parameter, and optionally indicate whether the ID is encoded.
"""
)
async def get_cheque_activation_count(cheque_id: Annotated[int | str, Query(alias='id', description="Unique identifier of the cheque")],
                                      encoded: Annotated[bool, Query(alias='e', description="Indicates whether the cheque ID is encoded")] = False,
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
    response_model=ChequeActivationDto,
    summary="Retrieve Paginated List of My Cheque Activations",
    description="""
Retrieves a paginated list of all cheque activations associated with the authenticated user.
Query parameters page and limit can be used to control pagination.
"""
)
async def get_my_cheque_activations_page(user_id=Depends(auth.auth_dependency),
                                         page: int = 1,
                                         limit: int = 1):
    result = await get_my_cheque_activations_page_impl(user_id, page, limit)
    return PaginatedResponse(result)
