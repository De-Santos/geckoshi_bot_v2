from protobuf.message_pb2 import Message
from variables import bot


async def message_observer(msg: Message):
    try:
        await bot.send_message(chat_id=msg.chat_id, text=msg.text)
    except Exception as e:
        print(e)
