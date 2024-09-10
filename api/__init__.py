from fastapi import APIRouter

from api import admin_api
from api import public_api

base_router = APIRouter()
base_router.include_router(public_api.router)
base_router.include_router(admin_api.router)

__all__ = ['base_router']
