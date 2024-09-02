from pydantic import BaseModel
from sqlalchemy import TypeDecorator
from sqlalchemy.dialects.postgresql import JSONB


class JSONEncodedDict(TypeDecorator):
    """Enables JSON storage by encoding and decoding on the fly."""
    impl = JSONB

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
        return value
