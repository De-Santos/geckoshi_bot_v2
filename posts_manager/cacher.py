from aiogram.types import Message

from variables import redis


def get_redis_key(channel_id: int) -> str:
    return f"post:{channel_id}"


async def cache_post(channel_id: int, message: Message) -> None:
    await redis.set(get_redis_key(channel_id), message.model_dump_json())


async def get_post(channel_id: int) -> Message | None:
    value = await redis.get(get_redis_key(channel_id))
    if value:
        return Message.model_validate_json(value)
    else:
        return None
