from pydantic import BaseModel


class UserRegistrationInfo(BaseModel):
    exists: bool
    registration_finished: bool = False
