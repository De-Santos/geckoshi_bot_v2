from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field


class NewPersonalChequeDto(BaseModel):
    name: Optional[str]
    amount: Decimal
    connected_to_user: int | None = Field(default=None)
    description: Optional[str] = Field(default=None)


class PersonalChequeDto(BaseModel):
    id: int
    name: str
    description: Optional[str]
    amount: Decimal | None = Field(default=None)
    connected_to_user: int | None = Field(default=None)
    created_at: datetime | None = Field(default=None)
    link: str | None = Field(default=None)
