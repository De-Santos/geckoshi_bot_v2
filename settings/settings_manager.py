import cache
from database import get_setting_by_id, SettingsKey, get_session


@cache.cacheable()
async def get_setting(key: SettingsKey) -> str | int:
    setting = get_setting_by_id(get_session(), key)
    if setting.int_val is not None:
        return setting.int_val
    elif setting.str_val is not None:
        return setting.str_val
