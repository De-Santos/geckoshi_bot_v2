import asyncio

from chat_processor.member import logger
from database import is_user_exists_by_tg, save_user, User
from handlers.referral import process_paying_for_referral
from providers.tg_arg_provider import TgArg, ArgType


async def validate_user(user_id: int, start_parameter: str | None) -> None:
    def get_ref() -> str | None:
        if start_parameter:
            return TgArg.get_arg(ArgType.REFERRAL, start_parameter)
        return None

    ref_id: int | None = get_ref()

    user_exists = await is_user_exists_by_tg(user_id, cache_id=user_id)

    if not user_exists and ref_id is not None:
        if await is_user_exists_by_tg(ref_id, cache_id=ref_id):
            try:
                await save_user(User(telegram_id=user_id, referred_by_id=ref_id))
                asyncio.create_task(process_paying_for_referral(user_id))
            except Exception as e:
                logger.error(f"Error saving user or processing referral: {e}", e)
        else:
            logger.warning("Referrer ID does not exist, skipping referral linking.")
    elif not user_exists:
        try:
            await save_user(User(telegram_id=user_id))
        except Exception as e:
            logger.error(f"Error saving user: {e}", e)
            raise e
