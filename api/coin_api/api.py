import logging
from typing import Annotated, Dict

from fastapi import APIRouter, Query
from starlette.responses import JSONResponse

from database import CurrencyType
from .impl import get_user_balance

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/coin",
    tags=["coin"],
)


@router.get(
    '/balance',
    response_model=Dict[CurrencyType, int],
    responses={
        200: {
            "status": "OK",
            "data": {}
        },
    }
)
async def get_balance_data(user_id: Annotated[int, Query(alias='id', description='The user id')]):
    result = await get_user_balance(user_id)
    return JSONResponse({"status": "OK",
                         "data": result})
