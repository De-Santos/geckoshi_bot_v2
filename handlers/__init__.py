from aiogram import Router

from filters.base_filters import ChatTypeFilter
from handlers.admin import admin_router
from handlers.bonus import router as bonus_router
from handlers.cheque import router as cheque_router
from handlers.exit import router as exit_router
from handlers.nft import router as nft_router
from handlers.p2p import router as p2p_router
from handlers.premium import router as premium_router
from handlers.profile import router as profile_router
from handlers.referral import router as referral_router
from handlers.self_member import router as bot_router
from handlers.settings import router as settings_router
from handlers.slots import router as slots_router
from handlers.start import router as start_router
from handlers.statistic import router as statistic_router
from handlers.task import router as task_router
from middleware.metadata_providers import LangProviderMiddleware

base_router = Router(name="base_router")

base_router.message.middleware(LangProviderMiddleware())
base_router.callback_query.middleware(LangProviderMiddleware())

base_router.message.filter(ChatTypeFilter())
base_router.callback_query.filter(ChatTypeFilter())

base_router.include_router(bot_router)
base_router.include_router(settings_router)
base_router.include_router(start_router)
base_router.include_router(referral_router)
base_router.include_router(profile_router)
base_router.include_router(exit_router)
base_router.include_router(premium_router)
base_router.include_router(cheque_router)
base_router.include_router(p2p_router)
base_router.include_router(slots_router)
base_router.include_router(nft_router)
base_router.include_router(admin_router)
base_router.include_router(task_router)
base_router.include_router(statistic_router)
base_router.include_router(bonus_router)

__all__ = [
    'base_router'
]
