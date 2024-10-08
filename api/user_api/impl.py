import io
from io import BytesIO

from PIL import Image
from aiogram.types import ChatFullInfo
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_user_by_tg, get_user_referrals_count, with_session, TransactionType
from transaction_manager.manager import select_transactions_sum_amount
from variables import bot
from .dto import UserDto


@with_session
async def get_user(user_id: int, s: AsyncSession = None) -> UserDto | None:
    user = await get_user_by_tg(user_id, s=s)
    ref_count = await get_user_referrals_count(user_id, s=s, cache_id=user_id)
    if user is None:
        return None
    dto = UserDto.model_validate(user, from_attributes=True)
    dto.referred_users_count = ref_count
    dto.withdrew = await select_transactions_sum_amount(user.telegram_id, TransactionType.WITHDRAW, s=s)
    return dto


async def get_tg_user(user_id: int) -> ChatFullInfo | None:
    return await bot.get_chat(user_id)


async def get_chat_img(chat_info: ChatFullInfo, img_filed_name: str) -> BytesIO:
    # Dynamically access the file_id using the provided field name
    file_id = getattr(chat_info.photo, img_filed_name)

    # Get the file for the chat photo
    file = await bot.get_file(file_id)

    # Download the photo as bytes
    photo_bytes = await bot.download_file(file.file_path)

    # Load it as an image using PIL
    img = Image.open(photo_bytes)

    # Prepare a BytesIO stream for the response
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    return img_byte_arr
