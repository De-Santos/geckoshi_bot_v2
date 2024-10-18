from typing import Any

from providers.tg_arg_provider import TgArg, ArgType
from variables import bot_url


def _get_bot_url_with_argument(argument: str) -> str:
    if argument.startswith("?start="):
        return bot_url + argument
    else:
        return bot_url + f"?start={argument}"


def generate(at: ArgType, val: Any) -> str:
    arg = TgArg(val)
    return _get_bot_url_with_argument(arg.encode(at))
