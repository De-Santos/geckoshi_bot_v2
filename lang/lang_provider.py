import logging
from typing import Union

from database import get_session, get_user_language
from lang.lang_based_provider import Lang
from variables import redis


def get_redis_lang_key(user_id: int) -> str:
    return f"lang:{user_id}"


async def cache_lang(user_tg_id: int, lang: Lang) -> None:
    await redis.set(get_redis_lang_key(user_tg_id), lang.value)


async def get_cached_lang(user_tg_id: int) -> Union[Lang, None]:
    lang_value = await redis.get(get_redis_lang_key(user_tg_id))
    if lang_value:
        return Lang(lang_value.decode('utf-8'))
    else:
        session = get_session()
        lang: Lang = get_user_language(session, user_tg_id)
        if lang is None:
            logging.exception(f"Language for user_tg_id is not available - {user_tg_id}")
            return None
        await cache_lang(user_tg_id, lang)
        return lang
