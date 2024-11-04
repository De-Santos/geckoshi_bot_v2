from fastapi import APIRouter

from . import activation
from . import personal

router = APIRouter(
    prefix="/cheque",
)

router.include_router(personal.router)
router.include_router(activation.router)

__all__ = ["router"]
