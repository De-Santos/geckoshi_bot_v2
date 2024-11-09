import logging

from fastapi import APIRouter, Depends
from starlette.responses import JSONResponse

import auth
from .dto import UserDto
from .impl import get_user, get_tg_user

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/user",
    tags=["user"]
)


@router.get(
    '/info',
    response_model=UserDto,
    summary="Get User Information",
    description=(
            "Fetch the information of the authenticated user. "
            "This endpoint requires a valid user authentication token. "
            "It returns details of the user."
    ),
    responses={
        200: {
            "status": "OK",
            "data": {}
        },
    }
)
async def get_user_info(user_id=Depends(auth.auth_dependency)):
    result = await get_user(user_id)

    return JSONResponse({"status": "OK",
                         "data": result.model_dump(mode='json')})


@router.get(
    '/chat',
    summary="Get User Chat Information",
    description=(
            "Retrieve the chat information associated with the authenticated user. "
            "A valid user authentication token is required to access this endpoint. "
            "It returns details of the telegram user."
    ),
    responses={
        200: {
            "status": "OK",
            "data": {}
        },
    }
)
async def get_user_chat_info(user_id=Depends(auth.auth_dependency)):
    result = await get_tg_user(user_id)
    return JSONResponse({"status": "OK",
                         "data": result.model_dump(mode='json')})
