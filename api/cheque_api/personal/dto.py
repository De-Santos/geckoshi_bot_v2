from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field


class NewPersonalChequeDto(BaseModel):
    name: Optional[str]
    amount: Decimal
    connected_to_user: int | None = Field(default=None)
    description: Optional[str] = Field(default=None)
