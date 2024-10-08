from pydantic import BaseModel, Field

from database import BetType


class BetResultDto(BaseModel):
    combination: str
    win_amount: int = Field(0, ge=0)
    bet_type: BetType
