import json
import logging
from functools import wraps
from typing import Callable

import humanfriendly

from variables import redis


def generate_cache_key(func: Callable, kwargs: dict) -> str:
    """
    Generate a cache key based on function name, args, and kwargs.
    """
    if 'cache_id' in kwargs:
        cache_id = kwargs.pop('cache_id')
        if callable(cache_id):
            cache_id = cache_id()
        return f"{func.__name__}:{str(cache_id)}"
    else:
        raise Exception("cache_id is not defined!")


def cacheable(ttl: str):
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            cache_key = generate_cache_key(func, kwargs)

            cached_result = await redis.get(cache_key)
            if cached_result:
                logging.info(f"cached call of function: {cache_key}")
                return json.loads(cached_result)

            result = await func(*args, **kwargs)
            seconds_ttl = humanfriendly.parse_timespan(ttl)
            logging.info(f"caching call of function: {cache_key}")
            json_obj = json.dumps(result)
            await redis.setex(cache_key, int(seconds_ttl), json_obj)
            return result

        return wrapper

    return decorator


async def drop_cache(func: Callable, **kwargs):
    key = generate_cache_key(func, kwargs)
    logging.info(f"delete cached call of function: {key}")
    await redis.delete(key)
