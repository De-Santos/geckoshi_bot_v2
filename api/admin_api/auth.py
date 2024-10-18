import logging

from fastapi import Header, HTTPException

from database import is_client_token_valid, CustomClientTokenType

logger = logging.getLogger(__name__)


async def auth_dependency(authorization: str = Header(None)):
    def error():
        logger.warning(f"Unauthorized access attempt with header: {authorization}")
        raise HTTPException(status_code=401, detail="Unauthorized")

    if authorization is None or authorization.strip() == "" or len(authorization.split()) == 1:
        error()

    token = authorization.split()[1]
    logger.info(f"Received token: {token}")

    if not await is_client_token_valid(id_=token, type_=CustomClientTokenType.PRIVATE, cache_id=token):
        logger.error(f"Token validation failed for token: {token}")
        error()

    logger.info(f"Token validation successful for token: {token}")
    return True
