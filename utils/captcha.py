import random
import typing as t
from io import BytesIO

from PIL.Image import Image
from PIL.ImageFilter import SMOOTH
from captcha.image import ImageCaptcha

from variables import captcha_length, captcha_val_set, captcha_answer_list_size, captcha_complexity_level

ColorTuple = t.Union[t.Tuple[int, int, int], t.Tuple[int, int, int, int]]


def generate_captcha_text() -> str:
    return ''.join(random.choices(captcha_val_set, k=captcha_length))


def generate_captcha_answer_list(captcha_code: str) -> list[(str, bool)]:
    result: list[str] = [captcha_code]
    for _ in range(captcha_answer_list_size - 1):
        result.append(generate_captcha_text())

    random.shuffle(result)
    return result


def generate_captcha(text: str = None) -> (str, BytesIO):
    captcha_text = generate_captcha_text() if text is None else text
    captcha_bytes = __generate_captcha(captcha_text)
    return captcha_text, captcha_bytes


def __generate_captcha(captcha_text: str) -> BytesIO:
    captcha = ImageCaptcha(width=280, height=90)
    background = random_color(238, 255)
    color = random_color(10, 200, random.randint(220, 255))
    im = captcha.create_captcha_image(captcha_text, color, background)
    captcha.create_noise_dots(im, color)
    captcha.create_noise_curve(im, color)
    add_dots(im, captcha, captcha_complexity_level)
    add_curve(im, captcha, captcha_complexity_level)
    im = im.filter(SMOOTH)

    out = BytesIO()
    im.save(out, format='png')
    out.seek(0)

    return out


def add_dots(im: Image, captcha: ImageCaptcha, lever: int) -> None:
    for _ in range(lever):
        __add_dots(im, captcha)


def __add_dots(im: Image, captcha: ImageCaptcha) -> None:
    color = random_color(10, 200, random.randint(220, 255))
    captcha.create_noise_dots(im, color)


def add_curve(im: Image, captcha: ImageCaptcha, lever: int) -> None:
    for _ in range(lever):
        __add_curve(im, captcha)


def __add_curve(im: Image, captcha: ImageCaptcha) -> None:
    color = random_color(10, 200, random.randint(220, 255))
    captcha.create_noise_curve(im, color)


def random_color(
        start: int,
        end: int,
        opacity: int | None = None) -> ColorTuple:
    red = random.randint(start, end)
    green = random.randint(start, end)
    blue = random.randint(start, end)
    if opacity is None:
        return red, green, blue
    return red, green, blue, opacity
