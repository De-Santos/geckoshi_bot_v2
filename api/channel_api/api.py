import logging
from typing import Annotated

from fastapi import APIRouter, Query, HTTPException, status

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/channel",
    tags=["channel"],
)


@router.get(
    '/link',
    summary="Get the last post link",
    description="""`MIGRATED TO -> '{HOSTPORT}/post-capturer'`""",
)
async def get_last_post_link():
    raise HTTPException(status_code=status.HTTP_418_IM_A_TEAPOT)


@router.get(
    '/photo',
    summary="Get the last post photo",
    description="""`MIGRATED TO -> '{HOSTPORT}/post-capturer'`""",
)
async def get_last_post_link(_: Annotated[int, Query(description='The photo resolution from worst (0) to best (3)', alias='r', ge=0, le=3)]):
    raise HTTPException(status_code=status.HTTP_418_IM_A_TEAPOT)
