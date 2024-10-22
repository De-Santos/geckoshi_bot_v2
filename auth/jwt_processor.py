import datetime
import os
from typing import Any

import jwt
from mako.exceptions import RuntimeException


def create_jwt_token(user_id: str) -> str:
    payload = {
        "sub": user_id,
        "exp": datetime.datetime.now() + datetime.timedelta(minutes=10)
    }
    token = jwt.encode(payload, os.getenv('SECRET_KEY'), algorithm="HS256")
    return token


def validate_jwt_token(token: str) -> Any:
    try:
        decoded_payload = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=["HS256"])
        return decoded_payload

    except jwt.ExpiredSignatureError:
        raise RuntimeException("Token has expired.")

    except jwt.InvalidTokenError:
        raise RuntimeException("Invalid token.")
