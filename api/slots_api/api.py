import logging
from typing import Annotated

from fastapi import APIRouter, Query, Depends
from starlette.responses import JSONResponse

import auth
from .dto import BetResultDto
from .impl import process_play

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/slots",
    tags=["slots"],
)


@router.post(
    '/play',
    response_model=BetResultDto,
    summary="Play Slot Game",
    description=(
            "Initiate a play action on the slot machine. This endpoint accepts a bet amount "
            "and returns the result of the play, including information about any winnings. "
            "A valid user authentication token is required to process the request."
    ),
    responses={
        200: {
            "status": "OK",
            "data": {}
        },
    }
)
async def get_user_info(amount: Annotated[int, Query(description='The bet amount')],
                        user_id=Depends(auth.auth_dependency)):
    result = await process_play(user_id, amount)

    return JSONResponse({"status": "OK",
                         "data": result.model_dump(mode='json')})
