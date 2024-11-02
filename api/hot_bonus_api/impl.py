import json
import logging
import os
import random
from datetime import datetime, UTC, timedelta

import humanfriendly
from fastapi import HTTPException
from redis import RedisError
from starlette import status

from database import TransactionOperation
from transaction_manager import make_transaction_from_system
from variables import redis
from .dto import HotBonus, NextHotBonusInfo

logger = logging.getLogger(__name__)


async def activate_hot_bonus_impl(user_id: int) -> HotBonus:
    available, _ = await get_bonus_status(user_id)
    if not available:
        raise HTTPException(status.HTTP_425_TOO_EARLY)
    bonus_amount = get_random_bonus_amount()
    await make_transaction_from_system(target=user_id,
                                       operation=TransactionOperation.INCREMENT,
                                       amount=bonus_amount,
                                       description="payment for hot bonus")
    cooldown = await cooldown_hot_bonus(user_id)
    return HotBonus(amount=bonus_amount, next_bonus_at=cooldown)


def get_random_bonus_amount():
    min_amount = int(os.getenv("HOT_BONUS_MIN", "900"))
    max_amount = int(os.getenv("HOT_BONUS_MAX", "3000"))

    return random.randint(min_amount, max_amount)


async def get_hot_bonus_info_impl(user_id: int) -> NextHotBonusInfo:
    available, t = await get_bonus_status(user_id)
    return NextHotBonusInfo(available=available, next_bonus_at=t)


async def cooldown_hot_bonus(user_id: int) -> datetime:
    ck = f"hot-bonus-{user_id}"

    now = datetime.now(UTC)
    cooldown_seconds = humanfriendly.parse_timespan(os.getenv('HOT_BONUS_COOLDOWN', '1h'))
    cooldown = now + timedelta(seconds=cooldown_seconds)

    try:
        json_obj = json.dumps(cooldown.isoformat())
        await redis.setex(ck, int(cooldown_seconds), json_obj)
    except RedisError as e:
        logging.error(f"Redis error while caching for key: {ck}: {e}")
        raise e
    return cooldown


async def get_bonus_status(user_id: int) -> (bool, datetime | None):
    ck = f"hot-bonus-{user_id}"
    try:
        cached_data = await redis.get(ck)
        if cached_data:
            try:
                # Attempt to load as JSON
                t: datetime = datetime.fromisoformat(json.loads(cached_data))
                return False, t
            except json.JSONDecodeError as e:
                logging.warning(f"Failed to decode cached JSON for key: {ck}")
                raise e
        else:
            return True, None
    except RedisError as e:
        logging.error(f"Redis error while fetching cache for key: {ck}: {e}")
        raise e
