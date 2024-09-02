from aiogram import Router

from filters.base_filters import AdminOnlyFilter
from handlers.admin.admin_processor import router as admin_processor_router
from handlers.admin.mailing import router as mailing_router
from handlers.admin.menu import router as admin_menu_router
from handlers.admin.referral import router as referral_router
from handlers.admin.task import router as admin_task_router

admin_router = Router(name="admin_base_router")

admin_router.message.filter(AdminOnlyFilter())
admin_router.callback_query.filter(AdminOnlyFilter())

admin_router.include_router(admin_processor_router)
admin_router.include_router(admin_menu_router)
admin_router.include_router(referral_router)
admin_router.include_router(mailing_router)
admin_router.include_router(admin_task_router)
