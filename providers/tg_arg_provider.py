from enum import Enum
from typing import Any


class ArgType(Enum):
    REFERRAL = ("r_", int)


class TgArg:
    arg_type: ArgType
    text: str
    parsed_value: Any

    def __init__(self, arg_type: ArgType, text: str):
        self.arg_type = arg_type
        self.text = text
        self.__parce_text()

    def __parce_text(self):
        prefix, type_func = self.arg_type.value
        if self.text.startswith(prefix):
            text_without_prefix = self.text[len(prefix):]
            try:
                self.parsed_value = type_func(text_without_prefix)
            except ValueError:
                self.parsed_value = None
        else:
            self.parsed_value = None

    def get(self) -> Any:
        return self.parsed_value

    @staticmethod
    def get_arg(arg_type: ArgType, text: str):
        args = text.split()
        if len(args) > 1:
            return TgArg(arg_type, args[1])
        else:
            return None
