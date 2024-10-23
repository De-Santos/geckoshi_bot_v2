from fastapi import APIRouter

from . import personal

router = APIRouter(
    prefix="/cheque",
    tags=["cheque"],
)

router.include_router(personal.router)

__all__ = ["router"]
