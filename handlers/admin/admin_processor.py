from aiogram import Router, F
from aiogram.types import Message

from filters.base_filters import UserExistsFilter
from keyboard_markup.custom_user_kb import get_reply_keyboard_kbm
from lang.lang_based_provider import get_message
from lang_based_variable import Lang, MessageKey

router = Router(name="admin_processor_router")


@router.message(F.text == "/becomeadmin", UserExistsFilter())
async def admin_menu_handler(message: Message, lang: Lang) -> None:
    await message.delete()
    await message.answer(text=get_message(MessageKey.ADMIN_NOW, lang),
                         reply_markup=get_reply_keyboard_kbm(lang, True))
