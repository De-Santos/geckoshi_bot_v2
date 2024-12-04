from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict

from database import ChequeActivationStatus
from ..dto import ChequeDto


class ChequeActivationDto(BaseModel):
    id: int
    cheque_info: ChequeDto | None = Field(default=None)
    user_id: int
    status: ChequeActivationStatus
    created_at: datetime
    processed_at: datetime | None = Field(default=None)
    failed_message: dict | None = Field(default=None)

    model_config = ConfigDict(
        use_enum_values=True,
        validate_assignment=True,
    )
