from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from database import TaskType, CurrencyType


class TaskDto(BaseModel):
    id: int
    type: TaskType
    title: Optional[str]
    text: Optional[str]
    markup: Optional[dict]
    coin_type: CurrencyType

    done_limit: Optional[int]
    coin_pool: Optional[int]
    done_reward: Optional[int]

    created_at: datetime
    expires_at: Optional[datetime]

    class Config:
        use_enum_values = True
