from lang_based_variable import KeyboardKey, Lang, MessageKey, message_data, keyboard_data, M


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


def format_string(template: str, *args, **kwargs) -> str:
    return template.format(*args, **kwargs)


def get_message(m: MessageKey, lng: Lang = None) -> str:
    if lng is None:
        msg = message_data[m]
    else:
        msg = message_data[lng][m]

    if msg is None or not isinstance(msg, str):
        raise ValueError("The message is not a valid string")

    return msg


def get_keyboard(k: KeyboardKey, lng: Lang = None) -> list[list["M"]]:
    if lng:
        d: dict = keyboard_data[lng][k]
    else:
        d: dict = keyboard_data[k]
    if d is None or not isinstance(d, list):
        raise ValueError("The message is not a valid dict")
    return d
