import os

from aiogram import Router, Bot
from aiogram.types import CallbackQuery, FSInputFile

from filters.base_filters import UserExistsFilter
from lang.lang_based_provider import get_message
from lang_based_variable import Lang, MessageKey, MenuToP2PCallback

router = Router(name="p2p_router")


@router.callback_query(MenuToP2PCallback.filter(), UserExistsFilter())
async def p2p_menu_handler(query: CallbackQuery, bot: Bot, lang: Lang) -> None:
    await query.message.delete()
    await bot.send_photo(chat_id=query.message.chat.id,
                         photo=FSInputFile(path=os.getenv("PHOTO_03_PATH")),
                         caption=get_message(MessageKey.SOON, lang))
