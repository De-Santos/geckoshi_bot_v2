from database import is_user_exists_by_tg, save_user, User
from providers.tg_arg_provider import TgArg, ArgType


async def validate_user(user_id: int, start_parameter: str | None) -> None:
    def ger_ref() -> str | None:
        if start_parameter:
            return TgArg.get_arg(ArgType.REFERRAL, start_parameter)
        return None

    if not await is_user_exists_by_tg(user_id, cache_id=user_id):
        await save_user(User(telegram_id=user_id, referred_by_id=ger_ref()))
