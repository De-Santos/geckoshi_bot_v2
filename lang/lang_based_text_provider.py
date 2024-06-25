from enum import Enum

import yaml

KEYBOARD = "kb"


class Lang(Enum):
    RU = "russian"
    EN = "english"
    TR = "turkish"
    DE = "german"


class MessageKey(Enum):
    START = "start"
    lANG_CHANGE = "lang_change"
    START_REQUIRE_SUBSCRIPTION = "start_required_subscription"
    START_REQUIRE_SUBSCRIPTION_SUCCESSFUL = "start_required_subscription_successful"


class KeyboardKey(Enum):
    START_REQUIRE_SUBSCRIPTION_KB = "start_required_subscription"


class KeyboardMetadata:
    text: str
    ref: str

    def __str__(self):
        return f"text='{self.text}', ref='{self.ref}'"

    def __init__(self, text: str, ref: str):
        self.text = text
        self.ref = ref

    @staticmethod
    def from_dict(d: dict):
        return KeyboardMetadata(d.get('text'), d.get('ref'))


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


def get_keyboard(k: KeyboardKey, lng: Lang) -> dict:
    d: dict = data[KEYBOARD][lng.value][k.value]
    if d is None or not isinstance(d, dict):
        raise ValueError("The message is not a valid dict")
    return d
