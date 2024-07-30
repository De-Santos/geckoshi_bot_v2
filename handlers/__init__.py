from aiogram import Router

from filters.base_filters import ChatTypeFilter
from handlers.exit import router as exit_router
from handlers.premium import router as premium_router
from handlers.profile import router as profile_router
from handlers.referral import router as referral_router
from handlers.self_member import router as bot_router
from handlers.settings import router as settings_router
from handlers.start import router as start_router
from middleware.metadata_providers import LangProviderMiddleware, IsAdminProviderMiddleware

base_router = Router(name="base_router")

base_router.message.middleware(LangProviderMiddleware())
base_router.callback_query.middleware(LangProviderMiddleware())

base_router.message.middleware(IsAdminProviderMiddleware())
base_router.callback_query.middleware(IsAdminProviderMiddleware())

base_router.message.filter(ChatTypeFilter())
base_router.callback_query.filter(ChatTypeFilter())

base_router.include_router(bot_router)
base_router.include_router(settings_router)
base_router.include_router(start_router)
base_router.include_router(referral_router)
base_router.include_router(profile_router)
base_router.include_router(exit_router)
base_router.include_router(premium_router)
