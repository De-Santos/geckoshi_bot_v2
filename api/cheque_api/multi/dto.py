from decimal import Decimal
from typing import Optional, List

from pydantic import BaseModel, Field


class NewMultiChequeDto(BaseModel):
    name: Optional[str]
    amount: Decimal
    activation_limit: int = Field(gt=0)
    require_subscriptions: List[int] = Field(default_factory=list)
    description: Optional[str] = Field(default=None)
    password: Optional[str] = Field(default=None)
