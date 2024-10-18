from io import BytesIO

from PIL import Image
from aiogram.types import ChatFullInfo

from variables import bot


async def get_chat_img(chat_info: ChatFullInfo, img_filed_name: str) -> BytesIO | None:
    # Dynamically access the file_id using the provided field name
    file_id = getattr(chat_info.photo, img_filed_name)
    if file_id is None:
        return None

    # Download the photo as bytes
    photo = await bot.download(file_id)
    if photo is None:
        return None

    # Load it as an image using PIL
    img = Image.open(photo.read())

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
