from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field, ConfigDict

from database import ChequeType, CurrencyType, ChequeActivationStatus


class ChequeDto(BaseModel):
    id: int
    name: str
    type: ChequeType
    amount: Decimal | None = Field(default=None)
    currency_type: CurrencyType
    description: str | None
    connected_to_user: int | None = Field(default=None)
    activation_limit: int
    created_at: datetime | None = Field(default=None)
    link: str | None = Field(default=None)

    model_config = ConfigDict(
        use_enum_values=True,
        validate_assignment=True,
    )


class ChequeActivationDto(BaseModel):
    id: int
    cheque_info: ChequeDto | None = Field(default=None)
    user_id: int
    status: ChequeActivationStatus
    created_at: datetime
    processed_at: datetime | None = Field(default=None)
    failed_message: str | None = Field(default=None)

    model_config = ConfigDict(
        use_enum_values=True,
        validate_assignment=True,
    )
