import logging
from typing import Annotated

from aiogram.types import ChatFullInfo
from fastapi import APIRouter, Query
from starlette.responses import JSONResponse, StreamingResponse

from .dto import UserDto
from .impl import get_user, get_tg_user, get_chat_img

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/user",
    tags=["user"],
)


@router.get(
    '/info',
    response_model=UserDto,
    responses={
        200: {
            "status": "OK",
            "data": {}
        },
    }
)
async def get_user_info(user_id: Annotated[int, Query(alias='id', description='The user id')]):
    result = await get_user(user_id)

    return JSONResponse({"status": "OK",
                         "data": result.model_dump()})


@router.get(
    '/chat',
    response_model=ChatFullInfo,
    responses={
        200: {
            "status": "OK",
            "data": {}
        },
    }
)
async def get_user_chat_info(user_id: Annotated[int, Query(alias='id', description='The user id')]):
    result = await get_tg_user(user_id)
    return JSONResponse({"status": "OK",
                         "data": result.model_dump()})


@router.get('/chat-photo')
async def get_user_info(user_id: Annotated[int, Query(alias='id', description='The user id')],
                        img_type: Annotated[str, Query(alias='type', description="img typs: 'small_file_id', 'big_file_id'")]):
    result: ChatFullInfo = await get_tg_user(user_id)
    img_bytes = await get_chat_img(result, img_type)
    return StreamingResponse(img_bytes, media_type="image/png")
