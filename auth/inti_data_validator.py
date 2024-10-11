import hashlib
import hmac
import json
import os
import time
from typing import Any, Dict

from mako.exceptions import RuntimeException
from pydantic import BaseModel
from starlette.datastructures import QueryParams


class ValidationResult(BaseModel):
    validated_data: Dict[str, str]
    user: Dict[str, Any]


def validate_telegram_webapp_data(telegram_init_data: QueryParams | dict) -> ValidationResult:
    bot_token = os.getenv('API_TOKEN')

    # Extract the hash
    hash_value = telegram_init_data.get('hash', None)
    if not hash_value:
        raise RuntimeException('Hash is missing from initData')

    data_without_hash = {k: v for k, v in telegram_init_data.items() if k != 'hash'}

    # Check auth_date
    auth_date = telegram_init_data.get('auth_date')
    if not auth_date:
        raise RuntimeException('auth_date is missing from initData')

    auth_timestamp = int(auth_date)
    current_timestamp = int(time.time())
    time_difference = current_timestamp - auth_timestamp
    five_minutes_in_seconds = 5 * 60

    if time_difference > five_minutes_in_seconds:
        raise RuntimeException('Telegram data is older than 5 minutes')

    # Generate the data check string
    data_check_string = "\n".join(
        [f"{key}={value}" for key, value in sorted(data_without_hash.items())]
    )

    # Create the secret key using HMAC SHA256
    secret_key = hmac.new(b'WebAppData', bot_token.encode(), hashlib.sha256).digest()

    # Calculate the hash
    calculated_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()

    # Compare the hash values
    if calculated_hash == hash_value:
        validated_data = {k: v for k, v in data_without_hash.items()}

        # Extract and parse the user data
        user_string = validated_data.get('user')
        if user_string:
            try:
                user = json.loads(user_string)
            except json.JSONDecodeError as error:
                message = f"Error parsing user data: {error}"
                raise RuntimeException(message)
        else:
            message = 'User data is missing'
            raise RuntimeException(message)

        return ValidationResult(validated_data=validated_data, user=user)

    else:
        raise RuntimeException('Hash validation failed')
