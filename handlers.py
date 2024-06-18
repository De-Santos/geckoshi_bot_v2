import logging

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from message_text_provider import MessageKey as msgK
from message_text_provider import get_message

router = Router(name=__name__)


@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    start_arguments = message.text.split()
    logging.info(str(start_arguments))
    await message.answer(get_message(msgK.START))


@router.message()
async def message_handler(message: Message) -> None:
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.answer("Nice try!")
