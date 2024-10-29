import os

from fastapi import APIRouter

import auth
from api import admin_api
from api import channel_api
from api import coin_api
from api import event_bonus_api
from api import hot_bonus_api
from api import language_api
from api import public_api
from api import slots_api
from api import task_api
from api import user_api

base_router = APIRouter()
base_router.include_router(public_api.router)
base_router.include_router(admin_api.router)
base_router.include_router(coin_api.router)
base_router.include_router(language_api.router)
base_router.include_router(slots_api.router)
base_router.include_router(user_api.router)
base_router.include_router(task_api.router)
base_router.include_router(auth.router)
base_router.include_router(channel_api.router)

if not bool(int(os.getenv("DISABLE_HOT_BONUS", "0"))):
    base_router.include_router(hot_bonus_api.router)

base_router.include_router(event_bonus_api.router)
__all__ = ['base_router']
