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
    arg_map: dict[str, ArgType] = {arg.prefix: arg for arg in ArgType}
    sqids: Sqids = Sqids(min_length=10)

    obj: Any
    parsed_value: T

    def __init__(self, obj: Any):
        self.obj = obj

    def parse(self) -> T:
        if not isinstance(self.obj, str):
            raise TypeError("TgArg cannot parse non-str object")
        self.__parse_text(self.obj)
        return self.parsed_value

    def __parse_text(self, text: str):
        for arg in self.arg_map.values():
            prefix, type_func, encoded = arg.prefix, arg.type_func, arg.encoded
            if text.startswith(prefix):
                text_without_prefix = text[len(prefix):]
                if encoded:
                    data = self.__decode(text_without_prefix)
                else:
                    data = text_without_prefix
                try:
                    self.parsed_value = type_func(data)
                except ValueError:
                    self.parsed_value = None
                break  # Exit loop after a successful match
            else:
                self.parsed_value = None

    def get(self) -> T:
        return self.parsed_value

    @staticmethod
    def get_arg(at: ArgType, text: str):
        args = text.split()
        if len(args) > 1:
            return TgArg(args[1])
        else:
            return None

    def encode(self, arg_type: ArgType) -> str:
        prefix, type_func, encoded = arg_type.prefix, arg_type.type_func, arg_type.encoded
        return f"{prefix}{self.__encode(type_func(self.obj))}"

    def __encode(self, obj: str | int):
        return self.sqids.encode([int(obj)])

    def __decode(self, obj: str):
        return self.sqids.decode(obj)[0]
