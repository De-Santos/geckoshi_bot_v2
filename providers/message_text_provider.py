from enum import Enum

import yaml


class Lang(Enum):
    RU = "russian"
    EN = "english"
    TR = "turkish"
    DE = "german"


class MessageKey(Enum):
    START = "start"


with open('message.yaml', 'r', encoding='utf-8') as file:
    data = yaml.safe_load(file)


def format_string(template: str, *args, **kwargs) -> str:
    return template.format(*args, **kwargs)


def get_message(m: MessageKey, lng: Lang = None) -> str:
    if lng is None:
        msg = data[m.value]
    else:
        msg = data[lng.value][m.value]

    if msg is None or not isinstance(msg, str):
        raise ValueError("The message is not a valid string")

    return msg
