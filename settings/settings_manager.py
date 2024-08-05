import cache
from database import get_setting_by_id, SettingsKey, get_session


@cache.cacheable()
async def get_setting(key: SettingsKey) -> str | int:
    setting = get_setting_by_id(get_session(), key)
    if setting.int_val is not None:
        return setting.int_val
    elif setting.str_val is not None:
        return setting.str_val


async def update_setting(key: SettingsKey, value: str | int) -> None:
    s = get_session()
    s.begin()
    setting = get_setting_by_id(s, key)
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
    s.commit()
