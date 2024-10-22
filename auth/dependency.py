import logging

from fastapi import Header, HTTPException
from mako.exceptions import RuntimeException

from .jwt_processor import validate_jwt_token

logger = logging.getLogger(__name__)


async def auth_dependency(authorization: str = Header(None, alias='Authorization')):
    def error():
        logger.warning(f"Unauthorized access attempt with header: {authorization}")
        raise HTTPException(status_code=401, detail="Unauthorized")

    if authorization is None or authorization.strip() == "" or len(authorization.split()) == 1:
        error()

    token = authorization.split()[1]
    logger.info(f"Received token: {token}")

    try:
        data = validate_jwt_token(token)
        logger.info(f"Token validation successful for token: {token}")
        return data['sub']
    except RuntimeException as e:
        logger.error(f"Token validation failed for token: {token}", e)
        raise HTTPException(status_code=401, detail=str(e))
