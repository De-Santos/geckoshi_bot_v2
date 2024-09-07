from fastapi import APIRouter

from api import public_api

base_router = APIRouter()
base_router.include_router(public_api.router)

__all__ = ['base_router']
