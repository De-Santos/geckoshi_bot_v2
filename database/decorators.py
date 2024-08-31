from functools import wraps
from typing import Callable, Optional


def with_session(func: Optional[Callable] = None, *, transaction: bool = False, override_name: str = "s"):
    from database.session_privider import get_session

    def decorator(f: Callable):
        @wraps(f)
        async def wrapper(*args, **kwargs):
            if kwargs.get(override_name) is not None:
                return await f(*args, **kwargs)

            session = get_session()
            if transaction:
                await session.begin()

            try:
                kwargs[override_name] = session

                result = await f(*args, **kwargs)

                await session.commit()

                return result
            except Exception as e:
                await session.rollback()
                raise e
            finally:
                await session.close()

        return wrapper

    # If func is not None, the decorator was used without arguments
    if func:
        return decorator(func)

    # If func is None, return the decorator for use with arguments
    return decorator
