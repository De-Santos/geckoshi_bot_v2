import uuid
from datetime import datetime
from decimal import Decimal
from typing import Optional, List

from pydantic import BaseModel, Field, ConfigDict

from database import ChequeType, CurrencyType


class ChequeDto(BaseModel):
    id: int
    name: Optional[str] = Field(default=None)
    type: ChequeType
    amount: Decimal | None = Field(default=None)
    currency_type: CurrencyType
    description: Optional[str] = Field(default=None)
    connected_to_user: Optional[int] = Field(default=None)
    activation_limit: int
    require_subscriptions: List[int] = Field(default_factory=list)
    created_at: datetime | None = Field(default=None)
    deleted_at: datetime | None = Field(default=None)
    payback_transaction_id: uuid.UUID | None = Field(default=None)
    link: str | None = Field(default=None)

    model_config = ConfigDict(
        use_enum_values=True,
        validate_assignment=True,
    )
