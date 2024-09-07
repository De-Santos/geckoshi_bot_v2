import logging
from typing import Annotated

from fastapi import APIRouter, Query, Depends
from starlette.responses import JSONResponse

from .auth import auth_dependency
from .dto import UserRegistrationInfo
from .impl import get_user_register_info

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/public",
    tags=["public-api"],
    dependencies=[Depends(auth_dependency)],
)


@router.get(
    '/user-exits',
    response_model=UserRegistrationInfo,
    summary="Check if a user exists",
    description="This endpoint checks if a user exists in the system using their user ID. "
                "It returns whether the user exists and if the registration is completed.",
    responses={
        200: {
            "description": "User information is returned",
            "content": {
                "application/json": {
                    "example": {
                        "exists": True,
                        "registration_finished": True
                    }
                }
            },
        },
    }
)
async def is_user_exits(user_id: Annotated[int, Query(alias='id', description='The user id')]):
    logger.info(f"Received request to check if user exists. User ID: {user_id}")

    result = await get_user_register_info(user_id)

    logger.info(f"User check result for user_id {user_id}: {result}")
    return JSONResponse({"status": "OK",
                         "data": result.model_dump()})
