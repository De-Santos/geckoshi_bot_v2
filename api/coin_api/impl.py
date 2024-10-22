from typing import Dict

from database import get_user_by_tg, CurrencyType


async def get_user_balance(user_id: int) -> Dict[CurrencyType, int] | None:
    user = await get_user_by_tg(user_id)
    if user is None:
        return None
    return {
        CurrencyType.GMEME.name: int(user.balance),
        CurrencyType.BMEME.name: int(user.bmeme_balance),
    }
