from aiogram.filters import Filter
from aiogram.types import Message, CallbackQuery

from database import is_user_exists_by_tg, get_session


class UserExistsFilter(Filter):
    async def __call__(self, message: Message = None, query: CallbackQuery = None) -> bool:
        if message is not None:
            tg_user_id = message.from_user.id
        elif query is not None:
            tg_user_id = query.from_user.id
        else:
            return False

        session = get_session()
        return await is_user_exists_by_tg(session, tg_user_id, cache_id=tg_user_id)
