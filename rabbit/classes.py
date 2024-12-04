import uuid

from pydantic import BaseModel, Field

from keyboard_markup.json_markup import deserialize_inline_keyboard_markup


class MessageDto(BaseModel):
    destination_id: int
    message: str | None
    button_markup: dict | None
    files: list[str] = Field(default_factory=list)
    mailing_id: int
    mailing_message_id: uuid.UUID
    is_last: bool

    def deserialize_button_markup(self):
        return deserialize_inline_keyboard_markup(self.button_markup)


class ActivationChequeDto(BaseModel):
    user_id: int
    cheque_id: int
    cheque_activation_id: int


class ChequePaybackDto(BaseModel):
    cheque_id: int
