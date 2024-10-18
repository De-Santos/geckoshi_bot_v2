from aiogram import Router
from aiogram.types import InlineQuery

from filters.base_filters import UserExistsFilter
from lang_based_variable import Lang

router = Router(name="inline_router")


@router.inline_query(UserExistsFilter())
async def inline_echo(query: InlineQuery, lang: Lang) -> None:
    pass
