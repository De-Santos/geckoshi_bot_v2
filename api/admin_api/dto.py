import uuid
from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field
from pydantic import UUID4

from database import TaskType, BotApiConfig, CurrencyType, Task


class TaskDTO(BaseModel):
    id: Optional[int] = None
    type: TaskType
    title: Optional[str] = None
    text: Optional[str] = None
    markup: Optional[dict] = None  # serialized 'InlineKeyboardMarkup'
    require_subscriptions: List[str] = Field(default_factory=list)

    api_configs: List[BotApiConfig] = Field(default_factory=list)

    coin_type: CurrencyType
    done_limit: Optional[int] = None
    coin_pool: Optional[int] = None
    done_reward: Optional[int] = None

    created_by_id: int
    created_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None

    deleted_by_id: Optional[int] = None
    deleted_at: Optional[datetime] = None

    trace_uuid: UUID4 = Field(default_factory=uuid.uuid4)

    def to_entity(self) -> Task:
        return Task(**self.model_dump())

    class Config:
        from_attributes = True
