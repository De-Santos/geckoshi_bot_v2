import functools
import logging

logger = logging.getLogger(__name__)


def try_marker(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            result = await func(*args, **kwargs)
            return result, True
        except Exception as e:
            logger.error(f"An error occurred in {func.__name__}: {e}")
            return None, False

    return wrapper


def trywrap_async(on_error_return):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                logger.error(f"Exception occurred in '{func.__name__}': {e}")
                return on_error_return

        return wrapper

    return decorator


def trywrap_sync(on_error_return):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.error(f"Exception occurred in '{func.__name__}': {e}")
                return on_error_return

        return wrapper

    return decorator


__all__ = ['try_marker', 'trywrap_async', 'trywrap_sync']
