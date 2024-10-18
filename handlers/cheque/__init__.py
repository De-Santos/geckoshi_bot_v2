from aiogram import Router

from . import menu
from . import personal_cheque
from . import management

public_base_router = Router(name="public_cheque_router")

public_base_router.include_router(menu.router)
public_base_router.include_router(personal_cheque.router)
public_base_router.include_router(management.router)
