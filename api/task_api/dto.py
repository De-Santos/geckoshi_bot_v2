from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from database import TaskType, CurrencyType


class TaskDto(BaseModel):
    id: int
    type: TaskType
    title: Optional[str] = None
    text: Optional[str] = None
    markup: Optional[dict] = None
    coin_type: CurrencyType

    done_limit: Optional[int] = None
    coin_pool: Optional[int] = None
    done_reward: Optional[int] = None

    created_at: datetime
    expires_at: Optional[datetime] = None

    class Config:
        orm_mode = True
