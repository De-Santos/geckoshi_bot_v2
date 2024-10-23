import logging
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from starlette.responses import JSONResponse

import auth
from .dto import NewPersonalChequeDto
from .impl import create_new_cheque_impl

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/personal",
    tags=["cheque"],
)


@router.post('')
async def create_new_cheque(dto: NewPersonalChequeDto,
                            user_id=Depends(auth.auth_dependency)):
    result = await create_new_cheque_impl(dto, user_id)
    return JSONResponse({
        "status": "OK",
        "data": result.model_dump(mode='json')
    })
