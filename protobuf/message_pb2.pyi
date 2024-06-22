from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Message(_message.Message):
    __slots__ = ("chat_id", "text")
    CHAT_ID_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    chat_id: int
    text: str
    def __init__(self, chat_id: _Optional[int] = ..., text: _Optional[str] = ...) -> None: ...
