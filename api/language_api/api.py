import logging
from typing import List, Annotated

from fastapi import APIRouter, Depends, Query
from starlette.responses import JSONResponse

import auth
from database import update_user_language
from lang.lang_provider import get_cached_lang, cache_lang
from lang_based_variable import Lang, message_data

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/language",
    tags=["language"],
)


@router.get(
    '/available',
    response_model=List[Lang],
    summary="Get Available Languages",
    description="Retrieve a list of languages available for the application. "
                "This endpoint does not require authentication and returns a list "
                "of supported languages in the system.",
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
    summary="Get Language Pack",
    description="Retrieve the language pack data specific to the user. "
                "This endpoint requires a valid authentication token to access the user's "
                "language preferences and returns localized messages.",
    responses={
        200: {
            "status": "OK",
            "data": {}
        },
    }
)
async def get_language_pack(user_id=Depends(auth.auth_dependency)):
    lang = await get_cached_lang(user_id)
    return JSONResponse({"status": "OK",
                         "data": {k.value: v for k, v in message_data[lang].items()}})


@router.post(
    '',
    response_model=bool,
    summary="Change User Language",
    description="This endpoint allows users to change their language preference. "
                "It takes the language code as a query parameter and updates the user's language "
                "setting in the database."
)
async def change_language(lang: Annotated[str, Query(description='The language')],
                          user_id=Depends(auth.auth_dependency)):
    try:
        await update_user_language(user_id, Lang(lang))
        await cache_lang(user_id, Lang(lang))
    except Exception as e:
        logger.error(e)
        return False
    return True
