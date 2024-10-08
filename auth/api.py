import logging

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


@router.get('/', response_model=AccessTokenResponse,
            summary="Create Access Token from Telegram initData",
            description="This endpoint receives Telegram's `initData` as query parameters from the mini application, "
                        "validates it, and generates an access token if valid.")
async def create_access_token(request: Request):
    params = request.query_params
    data: ValidationResult = validate_telegram_webapp_data(params)
    token: str = create_jwt_token(data.user.get('id'))
    return JSONResponse({"status": "OK",
                         "access_token": token})
