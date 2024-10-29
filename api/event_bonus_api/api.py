import logging
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from starlette.responses import JSONResponse

import auth
from .dto import ActivationEventBonusDto, EventBonusInfo, EventBonusDto
from .impl import activate_event_bonus_impl, get_event_bonus_info_impl, get_active_events_impl, get_event_bonus_balance_impl

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/event-bonus",
    tags=["event-bonus"],
)


@router.post(
    '',
    response_model=ActivationEventBonusDto,
    summary="Activate Event Bonus",
    description="Activate a bonus for a specific event. This endpoint allows a user to activate their bonus for a specific event using the event's ID.",
)
async def activate_event_bonus(event_id: Annotated[int, Query(description='Id of the event')],
                               user_id=Depends(auth.auth_dependency)):
    result = await activate_event_bonus_impl(event_id, user_id)
    return JSONResponse({"status": "OK",
                         "data": result.model_dump(mode='json')})


@router.get(
    '',
    response_model=EventBonusInfo,
    summary="Get Event Bonus Info",
    description="Retrieve information about a specific event bonus using the event ID. This endpoint indicates whether the user is eligible to claim the next bonus or if they need to wait for a cooldown.",
)
async def get_event_bonus_info(event_id: Annotated[int, Query(description='Id of the event')],
                               user_id=Depends(auth.auth_dependency)):
    result = await get_event_bonus_info_impl(event_id, user_id)
    return JSONResponse({"status": "OK",
                         "data": result.model_dump(mode='json')})


@router.get(
    '/balance',
    response_model=EventBonusInfo,
    summary="Get Event Bonus Balance",
    description="Retrieve the balance for a specific event by event ID. This endpoint allows a user to check their current bonus balance for an event.",
)
async def get_event_bonus_balance(event_id: Annotated[int, Query(description='Id of the event')],
                                  user_id=Depends(auth.auth_dependency)):
    result = await get_event_bonus_balance_impl(event_id, user_id)
    return JSONResponse({"status": "OK",
                         "data": result.model_dump(mode='json')})


@router.get(
    '/events',
    response_model=EventBonusDto,
    summary="Get Active Events",
    description="Retrieve a list of all currently active events. This endpoint returns information about each event.",
)
async def get_active_events(_=Depends(auth.auth_dependency)):
    results = await get_active_events_impl()
    return JSONResponse({"status": "OK",
                         "data": [e.model_dump(mode='json') for e in results]})
