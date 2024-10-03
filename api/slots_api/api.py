import logging
from typing import Annotated

from fastapi import APIRouter, Query
from starlette.responses import JSONResponse

from .dto import BetResultDto
from .impl import process_play

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/slots",
    tags=["slots"],
)


@router.get(
    '/play',
    response_model=BetResultDto,
    responses={
        200: {
            "status": "OK",
            "data": {}
        },
    }
)
async def get_user_info(user_id: Annotated[int, Query(alias='id', description='The user id')],
                        amount: Annotated[int, Query(description='The bet amount')]):
    result = await process_play(user_id, amount)

    return JSONResponse({"status": "OK",
                         "data": result.model_dump()})
