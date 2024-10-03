import logging
from typing import List, Annotated

from fastapi import APIRouter, Query
from starlette.responses import JSONResponse

from lang.lang_provider import get_cached_lang
from lang_based_variable import Lang, message_data

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/language",
    tags=["language"],
)


@router.get(
    '/available',
    response_model=List[Lang],
    responses={
        200: {
            "status": "OK",
            "data": {}
        },
    }
)
async def get_available_langs():
    return JSONResponse({"status": "OK",
                         "data": [lang.value for lang in Lang]})


@router.get(
    '/pack',
    response_model=dict,
    responses={
        200: {
            "status": "OK",
            "data": {}
        },
    }
)
async def get_language_pack(user_id: Annotated[int, Query(alias='id', description='The user id')]):
    lang = await get_cached_lang(user_id)
    return JSONResponse({"status": "OK",
                         "data": message_data[lang]})
