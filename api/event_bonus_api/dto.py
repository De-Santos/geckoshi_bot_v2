from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ActivationEventBonusDto(BaseModel):
    amount: int
    next_bonus_at: datetime


class EventBonusInfo(BaseModel):
    available: bool
    next_bonus_at: Optional[datetime]


class EventBalanceInfo(BaseModel):
    balance: int


class EventBonusDto(BaseModel):
    id: int
    name: Optional[str]
    start_datetime: datetime
    end_datetime: datetime
