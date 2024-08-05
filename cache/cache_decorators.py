import json
import logging
from functools import wraps
from typing import Callable, Any

import humanfriendly

from variables import redis


def generate_cache_key(func: Callable, args: tuple, kwargs: dict, just_function_name: bool = False) -> str:
    """
    Generate a cache key based on function name, args, and kwargs.
    """
    cache_id = kwargs.pop('cache_id', None)

    if just_function_name:
        return f"{func.__name__}"

    if cache_id is None:
        # Fall back to using a specific argument
        if len(args) > 0:
            cache_id = args[0]
        elif kwargs:
            cache_id = list(kwargs.values())[0]
        else:
            return f"{func.__name__}"

    if callable(cache_id):
        cache_id = cache_id()

    return f"{func.__name__}:{str(cache_id)}"


def cacheable(ttl: str = None, associate_none_as: Any = None, function_name_as_id: bool = False):
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            cache_key = generate_cache_key(func, args, kwargs, function_name_as_id)
            if not kwargs.pop('force', False):
                cached_result = await redis.get(cache_key)
                if cached_result:
                    logging.info(f"cached call of function: {cache_key}")
                    return json.loads(cached_result)
                elif associate_none_as is not None:
                    return associate_none_as

            result = await func(*args, **kwargs)
            logging.info(f"caching call of function: {cache_key}")
            json_obj = json.dumps(result)
            if ttl is not None:
                seconds_ttl = humanfriendly.parse_timespan(ttl)
                await redis.setex(cache_key, int(seconds_ttl), json_obj)
            else:
                await redis.set(cache_key, json_obj)
            return result

        return wrapper

    return decorator


async def drop_cache(func: Callable, *args, **kwargs):
    key = generate_cache_key(func, args, kwargs)
    logging.info(f"delete cached call of function: {key}")
    await redis.delete(key)
