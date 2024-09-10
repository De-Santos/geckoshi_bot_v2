from typing import Type

from pydantic import BaseModel
from sqlalchemy import TypeDecorator
from sqlalchemy.dialects.postgresql import JSONB


class JSONEncoded(TypeDecorator):
    """Enables JSON storage by encoding and decoding on the fly."""
    impl = JSONB

    def __init__(self, model_class: Type[BaseModel]):
        super().__init__()
        self.model_class = model_class

    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        if isinstance(value, BaseModel):
            # Convert Pydantic model to dict before storing
            return value.model_dump()
        return value

    def process_result_value(self, value, dialect):
        if value is None:
            return None
        return self.model_class.model_validate(value) if isinstance(value, dict) else None


class JSONEncodedList(TypeDecorator):
    """Enables JSON storage of a list of Pydantic models by encoding and decoding on the fly."""

    impl = JSONB

    def __init__(self, model_class: Type[BaseModel]):
        super().__init__()
        self.model_class = model_class

    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        if isinstance(value, list) and all(isinstance(item, BaseModel) for item in value):
            # Convert each Pydantic model to a dict before storing
            return [item.model_dump() for item in value]
        return value

    def process_result_value(self, value, dialect):
        if value is None:
            return None
        # Convert list of dicts back to list of Pydantic models
        return [self.model_class.model_validate(item) for item in value if isinstance(item, dict)]
