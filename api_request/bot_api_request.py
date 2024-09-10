import logging
from uuid import uuid4

import aiohttp
import jsonpath_ng
from jsonpath_ng.exceptions import JsonPathParserError

from api_request.exceptions import UnreachedJsonPathException
from database import BotApiConfig, ApiConfig

logger = logging.getLogger(__name__)


async def check_user_exists_via_api(user_id: int, bot_config: BotApiConfig) -> bool:
    trace_id = str(uuid4())

    logger.info(f"[{trace_id}] Processing ApiConfig with metadata: {bot_config.metadata}")
    api_config: ApiConfig = bot_config.api_config

    url: str = str(api_config.url)
    logger.info(f"[{trace_id}] Initial URL: {url}")

    for variable in api_config.path_variables:
        if variable.name == "id" or variable.name == "user_id":
            url = url.replace(f"{{{variable.name}}}", str(user_id))
        logger.debug(f"[{trace_id}] Replaced URL variable {variable.name} with {user_id}. Updated URL: {url}")
    logger.info(f"[{trace_id}] URL placeholders replaced. Updated URL: {url}")

    # Setup headers for the request
    headers = {}
    if api_config.authorization:
        headers["Authorization"] = api_config.authorization
        logger.debug(f"[{trace_id}] Authorization header set: {api_config.authorization}")

    logger.info(f"[{trace_id}] Making {api_config.method} request to {url} with headers {headers}")

    try:
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.request(api_config.method, url) as response:
                logger.info(f"[{trace_id}] Received response with status code: {response.status}")

                # Check if the response was successful
                response.raise_for_status()  # Will raise an exception for 4xx/5xx codes

                data = await response.json()
                logger.info(f"[{trace_id}] Response JSON: {data}")

                # Extract the expected value using the JSON path
                for expect in api_config.expectations:
                    logger.info(f"[{trace_id}] Checking JSON path: {expect.json_path} for expected value: {expect.expected_value}")
                    try:
                        jsonpath_expr = jsonpath_ng.parse(expect.json_path)
                        match = [m.value for m in jsonpath_expr.find(data)]
                    except JsonPathParserError:
                        logger.error(f"[{trace_id}] Invalid JSON path: {expect.json_path}")
                        raise UnreachedJsonPathException(f"Invalid JSON path: '{expect.json_path}'")

                    if not match or len(match) == 0:
                        logger.error(f"[{trace_id}] Unreachable path: '{expect.json_path}'")
                        raise UnreachedJsonPathException(f"Unreachable path: '{expect.json_path}'")

                    if match[0] != expect.expected_value:
                        logger.info(f"[{trace_id}] Expected value {expect.expected_value} not found. Actual: {match[0]}")
                        return False

    except aiohttp.ClientError as e:
        logger.error(f"[{trace_id}] HTTP request failed: {e}")
        return False
    except Exception as e:
        logger.error(f"[{trace_id}] An error occurred: {e}")
        return False

    return True
