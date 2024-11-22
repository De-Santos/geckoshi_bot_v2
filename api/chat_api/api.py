import logging
from io import BytesIO
from typing import Annotated, Union, Optional

from fastapi import APIRouter, Depends, Query
from starlette.responses import JSONResponse, StreamingResponse

import auth
from .impl import get_chat_full_info_impl, get_chat_img_impl, get_chat_short_info_impl

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/chat",
    tags=["chat"],
)


@router.get(
    '/full-info',
)
async def get_chat_full_info(chat_id: Annotated[Union[str, int], Query(description='The chat id, can be as int or as str -> "@channel_group_user"')],
                             _=Depends(auth.auth_dependency)):
    result = await get_chat_full_info_impl(chat_id)
    return JSONResponse({"status": "OK", **result})


@router.get(
    '/short-info',
)
async def get_chat_short_info(chat_id: Annotated[Union[str, int], Query(description='The chat id, can be as int or as str -> "@channel_group_user"')],
                              _=Depends(auth.auth_dependency)):
    result = await get_chat_short_info_impl(chat_id)
    return JSONResponse({"status": "OK", **result})


@router.get(
    '/img',
)
async def get_chat_img(file_id: Annotated[str, Query(description='The file id')],
                       force: Annotated[Optional[bool], Query(description='Use cached value or not')] = False,
                       _=Depends(auth.auth_dependency)):
    img_bytes = await get_chat_img_impl(file_id, cache_id=file_id, force=force)
    if img_bytes is None:
        return StreamingResponse(BytesIO(), status_code=204, media_type="image/png")
    return StreamingResponse(img_bytes, media_type="image/png")
