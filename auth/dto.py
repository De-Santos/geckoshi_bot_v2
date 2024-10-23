from typing import Optional

from pydantic import BaseModel


class AuthorizationDto(BaseModel):
    init_data: str
    start_argument: Optional[str]
