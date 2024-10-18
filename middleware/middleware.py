import asyncio
from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery

from database import save_activity_statistic, UserActivityContext


class ActivityStatisticMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]],
            event: CallbackQuery,
            data: Dict[str, Any]
    ) -> Any:
        prefix = event.data.split(':', 1)[0]
        context = UserActivityContext(callback_query_prefix=prefix)
        _ = asyncio.create_task(save_activity_statistic(event.from_user.id, context))
        return await handler(event, data)
