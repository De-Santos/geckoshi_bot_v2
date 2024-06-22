from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from database import get_user_by_tg, get_session, User, save_user, is_good_user, is_user_exists_by_tg
from message_processor.publisher import send_message
from providers.message_text_provider import MessageKey as msgK
from providers.message_text_provider import get_message
from providers.tg_arg_provider import TgArg, ArgType

router = Router(name=__name__)


@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    session = get_session()

    if await is_user_exists_by_tg(session, message.from_user.id, cache_id=message.from_user.id) is None:
        ref_arg = TgArg.get_arg(ArgType.REFERRAL, message.text)
        if ref_arg is not None and is_good_user(session, ref_arg.get()):
            user = User(telegram_id=message.from_user.id, referred_by_id=ref_arg.get())
        else:
            user = User(telegram_id=message.from_user.id)
        save_user(session, user)
    await message.answer(get_message(msgK.START))
    for i in range(20):
        await send_message(message.copy(), text="hello")


@router.message()
async def message_handler(message: Message) -> None:
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.answer("Nice try!")
