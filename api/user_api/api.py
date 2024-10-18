import logging
from io import BytesIO
from typing import Annotated

from aiogram.types import ChatFullInfo
from fastapi import APIRouter, Query, Depends
from starlette.responses import JSONResponse, StreamingResponse

import auth
from chat_processor.chat_image import get_chat_img
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


@router.get(
    '/chat-photo',
    summary="Get User Chat Photo",
    description=(
            "Fetch the chat photo for the user's chat. This endpoint requires the "
            "type of the image as a query parameter (e.g., 'small_file_id' or 'big_file_id'). "
            "A valid user authentication token is required. The response will return the "
            "requested image in PNG format."
    )
)
async def get_user_info(img_type: Annotated[str, Query(alias='type', description="img types: 'small_file_id', 'big_file_id'")],
                        user_id=Depends(auth.auth_dependency)):
    result: ChatFullInfo = await get_tg_user(user_id)
    img_bytes = await get_chat_img(result, img_type)
    if img_bytes is None:
        return StreamingResponse(BytesIO(), status_code=204, media_type="image/png")
    return StreamingResponse(img_bytes, media_type="image/png")
