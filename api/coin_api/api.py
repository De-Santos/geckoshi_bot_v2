import logging
from typing import Dict

from fastapi import APIRouter, Depends
from starlette.responses import JSONResponse

import auth
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
    summary="Get User Balance",
    description="Retrieve the current balance of the user identified by the JWT token. "
                "This endpoint requires a valid authentication token to access the user's balance.",
    responses={
        200: {
            "status": "OK",
            "data": {}
        },
    }
)
async def get_balance_data(user_id=Depends(auth.auth_dependency)):
    result = await get_user_balance(user_id)
    return JSONResponse({"status": "OK",
                         "data": result})
