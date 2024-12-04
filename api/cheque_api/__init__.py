from fastapi import APIRouter

from . import activation
from . import multi
from . import personal

router = APIRouter(
    prefix="/cheque",
)

router.include_router(personal.router)
router.include_router(multi.router)
router.include_router(activation.router)

__all__ = ["router"]
