from contextlib import asynccontextmanager

import database
from variables import redis


@asynccontextmanager
async def acquire_lock(key: tuple, max_duration: int = None):
    """
    Context manager to acquire and automatically release a Redis lock.

    :param key: Tuple representing the lock key.
    :param max_duration: Duration in seconds for the lock to persist.
    """
    lock_key = "lock:" + ":".join(map(str, key))  # Prefix 'lock:' and join with ':'
    lock_value = str(database.now())

    try:
        await redis.set(lock_key, lock_value, ex=max_duration)
        yield
    finally:
        await redis.delete(lock_key)


async def is_lock_persisting(key: tuple) -> tuple:
    """
    Checks if a lock is persisting in Redis.

    :param key: Tuple representing the lock key.
    :return: A tuple (bool, float) where the first value indicates if the lock exists,
             and the second is the remaining TTL in seconds.
    """
    lock_key = "lock:" + ":".join(map(str, key))  # Prefix 'lock:' and join with ':'
    ttl = await redis.ttl(lock_key)
    return (ttl > 0, ttl) if ttl > 0 else (False, None)


async def remove_lock(key: tuple) -> bool:
    """
    Removes a lock from Redis.

    :param key: Tuple representing the lock key.
    :return: True if the lock was removed, False if it did not exist.
    """
    lock_key = "lock:" + ":".join(map(str, key))  # Prefix 'lock:' and join with ':'
    return await redis.delete(lock_key) > 0


__all__ = [
    "acquire_lock",
    "is_lock_persisting",
    "remove_lock",
]
