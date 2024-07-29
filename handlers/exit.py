from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from filters.base_filters import UserExistsFilter
from lang_based_variable import Exit

router = Router(name="exit_router")


@router.message(F.text == "/exit", UserExistsFilter())
@router.callback_query(Exit.filter(), UserExistsFilter())
async def exit_handler(query: CallbackQuery, state: FSMContext) -> None:
    await query.message.delete()
    await state.clear()
