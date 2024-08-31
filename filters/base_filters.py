from aiogram.enums import ChatType
from aiogram.filters import Filter
from aiogram.types import Message, CallbackQuery

from database import is_user_exists_by_tg, is_good_user_by_tg, has_premium, is_admin


class UserExistsFilter(Filter):
    async def __call__(self, message: Message = None, query: CallbackQuery = None) -> bool:
        if message is not None:
            tg_user_id = message.from_user.id
        elif query is not None:
            tg_user_id = query.from_user.id
        else:
            return False

        return await is_user_exists_by_tg(tg_user_id, cache_id=tg_user_id)


class IsPremiumUser(Filter):
    async def __call__(self, message: Message = None, query: CallbackQuery = None) -> bool:
        if message is not None:
            tg_user_id = message.from_user.id
        elif query is not None:
            tg_user_id = query.from_user.id
        else:
            return False

        return await has_premium(tg_user_id, cache_id=tg_user_id)


class IsGoodUserFilter(Filter):
    async def __call__(self, message: Message = None, query: CallbackQuery = None) -> bool:
        if message is not None:
            tg_user_id = message.from_user.id
        elif query is not None:
            tg_user_id = query.from_user.id
        else:
            return False

        return await is_good_user_by_tg(tg_user_id, cache_id=tg_user_id)


class ChatTypeFilter(Filter):
    async def __call__(self, obj) -> bool:
        if obj is not None and isinstance(obj, Message):
            chat_type = obj.chat.type
        elif obj is not None and isinstance(obj, CallbackQuery):
            chat_type = obj.message.chat.type
        else:
            return False

        return chat_type == ChatType.PRIVATE


class AdminOnlyFilter(Filter):
    async def __call__(self, message: Message = None, query: CallbackQuery = None) -> bool:
        if message is not None:
            tg_user_id = message.from_user.id
        elif query is not None:
            tg_user_id = query.from_user.id
        else:
            return False

        return await is_admin(tg_user_id, cache_id=tg_user_id)
