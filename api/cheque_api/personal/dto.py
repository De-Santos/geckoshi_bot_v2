from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel


class NewPersonalChequeDto(BaseModel):
    name: Optional[str]
    amount: Decimal


class PersonalChequeDto(BaseModel):
    id: int
    name: str
    amount: Decimal
    connected_to_user: int
    created_at: datetime
    link: str
