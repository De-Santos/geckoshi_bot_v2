from sqlalchemy.ext.asyncio import AsyncSession

import cache
from database import get_setting_by_id, SettingsKey, with_session


@cache.cacheable()
async def get_setting(key: SettingsKey) -> str | int:
    setting = await get_setting_by_id(key)
    if setting.int_val is not None:
        return setting.int_val
    elif setting.str_val is not None:
        return setting.str_val


@with_session(transaction=True)
async def update_setting(key: SettingsKey, value: str | int, s: AsyncSession = None) -> None:
    setting = get_setting_by_id(key, s=s)
    if isinstance(value, int):
        setting.int_val = value
        setting.str_val = None
    elif isinstance(value, str):
        setting.int_val = None
        setting.str_val = value
    else:
        setting.int_val = None
        setting.str_val = None

    await cache.drop_cache(get_setting, key)
