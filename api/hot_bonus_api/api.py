import logging

from fastapi import APIRouter, Depends
from starlette.responses import JSONResponse

import auth
from .dto import HotBonus, NextHotBonusInfo
from .impl import activate_hot_bonus_impl, get_hot_bonus_info_impl

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/hot-bonus",
    tags=["hot-bonus"],
)


@router.post(
    '',
    response_model=HotBonus,
)
async def activate_hot_bonus(user_id=Depends(auth.auth_dependency)):
    result = await activate_hot_bonus_impl(user_id)
    return JSONResponse({"status": "OK",
                         "data": result.model_dump(mode='json')})


@router.get('', response_model=NextHotBonusInfo)
async def get_hot_bonus_info(user_id=Depends(auth.auth_dependency)):
    result = await get_hot_bonus_info_impl(user_id)
    return JSONResponse({"status": "OK",
                         "data": result.model_dump(mode='json')})
