from aiogram import Router

from handlers.admin.admin_processor import router as admin_processor_router
from handlers.admin.menu import router as admin_menu_router
from handlers.admin.referral import router as referral_router

from filters.base_filters import AdminOnlyFilter
from middleware.metadata_providers import IsAdminProviderMiddleware

admin_router = Router(name="admin_base_router")

admin_router.message.middleware(IsAdminProviderMiddleware())
admin_router.callback_query.middleware(IsAdminProviderMiddleware())

admin_router.message.filter(AdminOnlyFilter())
admin_router.callback_query.filter(AdminOnlyFilter())

admin_router.include_router(admin_processor_router)
admin_router.include_router(admin_menu_router)
admin_router.include_router(referral_router)
