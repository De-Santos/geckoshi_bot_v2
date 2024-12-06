from enum import Enum
from typing import Any, TypeVar, Generic, Callable

from sqids import Sqids

T = TypeVar('T')


class ArgType(Enum):
    REFERRAL = ("r_", int, False)
    CHEQUE = ("c_", int, True)

    def __init__(self, prefix: str, type_func: Callable, encoded: bool):
        self.prefix = prefix
        self.type_func = type_func
        self.encoded = encoded


class TgArg(Generic[T]):
    arg_map = {arg.prefix: arg for arg in ArgType}
    sqids = Sqids(min_length=10)

    def __init__(self, obj: Any):
        self.obj = obj
        self.parsed_value: T | None = None

    def parse(self) -> T | None:
        for arg in self.arg_map.values():
            if self.obj.startswith(arg.prefix):
                self.parsed_value = self._parse_with_arg_type(arg)
                break
        return self.parsed_value

    def _parse_with_arg_type(self, arg: ArgType) -> T | None:
        text_without_prefix = self.obj[len(arg.prefix):]
        data = self._decode(text_without_prefix) if arg.encoded else text_without_prefix
        try:
            return arg.type_func(data)
        except ValueError:
            return None

    def get(self) -> T | None:
        return self.parsed_value

    def get_type(self) -> ArgType | None:
        for arg in self.arg_map.values():
            if self.obj.startswith(arg.prefix):
                return arg
        return None

    @staticmethod
    def get_arg(at: ArgType, text: str):
        args = text.split()
        if len(args) > 1 and args[1].startswith(at.prefix):
            return TgArg(args[1])
        return None

    def encode(self, arg_type: ArgType) -> str:
        data = str(self.obj)  # Ensure the object can be stringified
        encoded_data = self._encode(data) if arg_type.encoded else data
        return f"{arg_type.prefix}{encoded_data}"

    def _encode(self, obj: str | int) -> str:
        return self.sqids.encode([int(obj)])

    def _decode(self, obj: str) -> str:
        decoded = self.sqids.decode(obj)
        return str(decoded[0])
