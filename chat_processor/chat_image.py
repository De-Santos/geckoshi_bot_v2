import logging
from io import BytesIO

from PIL import Image
from aiogram.types import ChatFullInfo

from variables import bot

logger = logging.getLogger(__name__)


async def get_chat_img(chat_info: ChatFullInfo, img_filed_name: str) -> BytesIO | None:
    file_id = getattr(chat_info.photo, img_filed_name, None)
    if file_id is None:
        return None

    # Download the photo as bytes
    photo = await bot.download(file_id)
    if photo is None:
        return None

    # Check if the downloaded photo is valid and readable
    try:
        img = Image.open(photo)
    except Exception as e:
        logger.error(f"Failed to open image: {e}")
        return None

    # Prepare a BytesIO stream for the response
    img_byte_arr = BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    return img_byte_arr


async def get_chat_img_by_chat_id(chat_id: int, img_filed_name: str) -> BytesIO | None:
    chat = await bot.get_chat(chat_id)
    if chat is None:
        return None
    return await get_chat_img(chat, img_filed_name)
