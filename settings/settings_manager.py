from sqlalchemy.orm import Session

import cache
from database import get_setting_by_id, SettingsKey


@cache.cacheable()
def get_setting(session: Session, key: SettingsKey) -> str | int:
    setting = get_setting_by_id(session, key)
    if setting.int_val is not None:
        return setting.int_val
    elif setting.str_val is not None:
        return setting.str_val
