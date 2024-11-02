import json
import logging
import random
from datetime import datetime, UTC, timedelta

import humanfriendly
from fastapi import HTTPException
from redis import RedisError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import make_transient
from starlette import status

from database import get_active_events, get_active_event_by_id, with_session, EventBonusActivation, EventBonus, get_total_amount_by_user_event
from variables import redis
from .dto import ActivationEventBonusDto, EventBonusInfo, EventBonusDto, EventBalanceInfo

logger = logging.getLogger(__name__)


async def activate_event_bonus_impl(event_id: int, user_id: int) -> ActivationEventBonusDto:
    available, _ = await get_bonus_status(event_id, user_id)
    if not available:
        raise HTTPException(status.HTTP_425_TOO_EARLY)
    event = await get_event(event_id)
    bonus_amount = await get_random_bonus_amount(event)
    cooldown = await cooldown_event_bonus(event, user_id)
    await save_event_activation(user_id, event_id, bonus_amount)
    return ActivationEventBonusDto(amount=bonus_amount, next_bonus_at=cooldown)


@with_session
async def save_event_activation(user_id: int, event_id: int, amount: int, s: AsyncSession = None) -> EventBonusActivation:
    eba = EventBonusActivation(
        user_id=user_id,
        amount=amount,
        event_bonus_id=event_id,
    )
    s.add(eba)
    return eba


async def get_event(event_id: int) -> EventBonus:
    event = await get_active_event_by_id(event_id)
    if not event:
        raise HTTPException(status.HTTP_400_BAD_REQUEST)
    make_transient(event)
    return event


async def get_random_bonus_amount(event: EventBonus) -> int:
    return random.randint(event.min_win, event.max_win)


async def get_event_bonus_info_impl(event_id: int, user_id: int) -> EventBonusInfo:
    available, t = await get_bonus_status(event_id, user_id)
    return EventBonusInfo(available=available, next_bonus_at=t)


async def get_event_bonus_balance_impl(event_id: int, user_id: int) -> EventBalanceInfo:
    balance = await get_total_amount_by_user_event(user_id, event_id)
    return EventBalanceInfo(balance=balance)


async def get_active_events_impl() -> list[EventBonusDto]:
    active_events = await get_active_events()
    result = []
    for event in active_events:
        result.append(EventBonusDto.model_validate(event, from_attributes=True))
    return result


async def cooldown_event_bonus(event: EventBonus, user_id: int) -> datetime:
    ck = f"event-bonus-{event.id}-{user_id}"

    now = datetime.now(UTC)
    cooldown_seconds = humanfriendly.parse_timespan(event.cooldown)
    cooldown = now + timedelta(seconds=cooldown_seconds)

    try:
        json_obj = json.dumps(cooldown.isoformat())
        await redis.setex(ck, int(cooldown_seconds), json_obj)
    except RedisError as e:
        logging.error(f"Redis error while caching for key: {ck}: {e}")
        raise e
    return cooldown


async def get_bonus_status(event_id: int, user_id: int) -> (bool, datetime | None):
    ck = f"event-bonus-{event_id}-{user_id}"
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
