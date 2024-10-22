import json
import logging
from functools import wraps
from typing import Callable, Any

import dill
import humanfriendly
from redis import RedisError

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


def cacheable(ttl: str = None, associate_none_as: Any = None, function_name_as_id: bool = False, save_as_blob: bool = False, cache_result_ignore_val: Any = None):
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            cache_key = generate_cache_key(func, args, kwargs, function_name_as_id)
            if not kwargs.pop('force', False):
                try:
                    cached_result = await redis.get(cache_key)
                    if cached_result:
                        logging.info(f"cached call of function: {cache_key}")
                        if save_as_blob:
                            try:
                                # Attempt to load as binary
                                return dill.loads(cached_result)
                            except dill.UnpicklingError:
                                logging.error(f"Failed to decode cached blob for key: {cache_key}")
                                return associate_none_as
                        else:
                            try:
                                # Attempt to load as JSON
                                return json.loads(cached_result)
                            except json.JSONDecodeError:
                                logging.warning(f"Failed to decode cached JSON for key: {cache_key}")
                                return associate_none_as
                except RedisError as e:
                    logging.error(f"Redis error while fetching cache for key: {cache_key}: {e}")
                    return associate_none_as

            try:
                result = await func(*args, **kwargs)
                if cache_result_ignore_val == result:
                    logging.info(f"caching call of function - ignored: {cache_key}")
                    return result
                logging.info(f"caching call of function: {cache_key}")

                if save_as_blob:
                    # Save result as a binary blob
                    blob_obj = dill.dumps(result)
                    if ttl is not None:
                        seconds_ttl = humanfriendly.parse_timespan(ttl)
                        await redis.setex(cache_key, int(seconds_ttl), blob_obj)
                    else:
                        await redis.set(cache_key, blob_obj)
                else:
                    # Save result as JSON
                    try:
                        json_obj = json.dumps(result)
                        if ttl is not None:
                            seconds_ttl = humanfriendly.parse_timespan(ttl)
                            await redis.setex(cache_key, int(seconds_ttl), json_obj)
                        else:
                            await redis.set(cache_key, json_obj)
                    except (TypeError, OverflowError):
                        # Fallback to saving as binary if JSON serialization fails
                        blob_obj = dill.dumps(result)
                        if ttl is not None:
                            seconds_ttl = humanfriendly.parse_timespan(ttl)
                            await redis.setex(cache_key, int(seconds_ttl), blob_obj)
                        else:
                            await redis.set(cache_key, blob_obj)

                return result
            except Exception as e:
                logging.error(f"Error during function execution: {e}")
                raise e

        return wrapper

    return decorator


async def drop_cache(func: Callable, *args, **kwargs):
    key = generate_cache_key(func, args, kwargs)
    logging.info(f"delete cached call of function: {key}")
    await redis.delete(key)
