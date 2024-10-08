from datetime import datetime

from pydantic import BaseModel, Field

from lang_based_variable import Lang


class UserDto(BaseModel):
    telegram_id: int
    balance: int = Field(default=0)
    bmeme_balance: int = Field(default=0)
    withdrew: int = Field(default=0)
    blocked: bool = Field(default=False)
    language: Lang = Field(default=Lang.EN)
    is_admin: bool = Field(default=False)
    is_premium: bool = Field(default=False)
    referred_users_count: int = Field(default=0)
    is_bot_start_completed: bool = Field(default=False)
    created_at: datetime
