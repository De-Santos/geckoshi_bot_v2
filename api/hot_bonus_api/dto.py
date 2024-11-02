from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel


class HotBonus(BaseModel):
    amount: Decimal
    next_bonus_at: datetime


class NextHotBonusInfo(BaseModel):
    available: bool
    next_bonus_at: Optional[datetime]
