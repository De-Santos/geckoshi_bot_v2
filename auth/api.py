import logging
from urllib.parse import urlparse, parse_qs

from fastapi import APIRouter
from pydantic import BaseModel
from starlette.requests import Request
from starlette.responses import JSONResponse

from .inti_data_validator import validate_telegram_webapp_data, ValidationResult
from .jwt_processor import create_jwt_token

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


class AccessTokenResponse(BaseModel):
    status: str
    access_token: str


@router.get('', response_model=AccessTokenResponse,
            summary="Create Access Token from Telegram initData",
            description="This endpoint receives Telegram's `initData` as query parameters from the mini application, "
                        "validates it, and generates an access token if valid.")
async def create_access_token(request: Request):
    params = request.query_params
    data: ValidationResult = validate_telegram_webapp_data(params)
    token: str = create_jwt_token(data.user.get('id'))
    return JSONResponse({"status": "OK",
                         "access_token": token})


@router.post('/v2', response_model=AccessTokenResponse,
             summary="Create Access Token from Telegram initData",
             description="This endpoint receives Telegram's `initData` as query parameters from the mini application, "
                         "validates it, and generates an access token if valid.")
async def create_access_token_v2(request: Request):
    params = request.query_params
    data: ValidationResult = validate_telegram_webapp_data(params)
    token: str = create_jwt_token(data.user.get('id'))
    return JSONResponse({"status": "OK",
                         "access_token": token})


@router.post('/v3', response_model=AccessTokenResponse,
             summary="Create Access Token from Telegram initData",
             description="This endpoint receives Telegram's `initData` as query parameters from the mini application, "
                         "validates it, and generates an access token if valid.")
async def create_access_token_v3(request: Request):
    data: dict = await request.json()
    parsed_data = {k: v[0] for k, v in parse_qs(urlparse(f"?{data.get('data')}").query).items()}
    data: ValidationResult = validate_telegram_webapp_data(parsed_data)
    token: str = create_jwt_token(data.user.get('id'))
    return JSONResponse({"status": "OK",
                         "access_token": token})
