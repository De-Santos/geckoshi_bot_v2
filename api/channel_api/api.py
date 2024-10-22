import logging
from io import BytesIO
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from starlette.responses import JSONResponse, StreamingResponse

import auth
from .impl import get_post_link, get_post_photo

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/channel",
    tags=["channel"],
)


@router.get(
    '/link',
    summary="Get the last post link",
    description="""    
Retrieves the link to the most recent post in a specified channel.

This endpoint fetches the latest post link from a pre-configured channel.
It requires user authentication and returns the post link if available.
""",
)
async def get_last_post_link(_=Depends(auth.auth_dependency)):
    result = await get_post_link()
    return JSONResponse({"status": "OK",
                         "data": result})


@router.get(
    '/photo',
    summary="Get the last post photo",
    description="""
Retrieves the photo from the most recent post in a channel.

This endpoint fetches the photo attached to the latest post in a channel.
The resolution can be specified using the 'r' query parameter, with a range from 0 (worst) to 3 (best).
If no photo is found, a `204 No Content` status is returned.
""",
)
async def get_last_post_link(resolution: Annotated[int, Query(description='The photo resolution from worst (0) to best (3)', alias='r', ge=0, le=3)],
                             _=Depends(auth.auth_dependency)):
    img_bytes = await get_post_photo(resolution)
    if img_bytes is None:
        return StreamingResponse(BytesIO(), status_code=204, media_type="image/png")
    return StreamingResponse(img_bytes, media_type="image/png")
