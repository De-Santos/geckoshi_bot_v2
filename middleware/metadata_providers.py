from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message

from database import is_user_admin_by_tg_id, has_premium
from lang.lang_provider import get_cached_lang


class LangProviderMiddleware(BaseMiddleware):

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        data['lang'] = await get_cached_lang(event.from_user.id)
        return await handler(event, data)


class IsAdminProviderMiddleware(BaseMiddleware):

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        data['is_admin'] = await is_user_admin_by_tg_id(event.from_user.id, cache_id=event.from_user.id)
        return await handler(event, data)


class IsPremiumUserMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        data['is_premium'] = await has_premium(event.from_user.id, cache_id=event.from_user.id)
        return await handler(event, data)
