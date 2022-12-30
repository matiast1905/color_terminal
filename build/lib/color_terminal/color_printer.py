from cgitb import text
import pickle
from math import sqrt
from typing import Optional
from pathlib import Path

esc = "\033["
# Reset all colors sequence
reset = esc + "0m"
# Text color
txt_color = esc + "38;5;{}m"
# Bold color text
bold_color = esc + "1;38;5;{}m"
# Bold text without color
bold_text = esc + "1m"
# Background color
bg_color = esc + "48;5;{}m"

with open(Path(__file__).parent / "colors_dict.pkl", "rb") as f:
    colors_dictionary = pickle.load(f)


def cprint(
    *values,
    text_color: Optional[str | tuple[int, int, int]] = None,
    background_color: Optional[str | tuple[int, int, int]] = None,
    bold: bool = False,
    sep=" ",
    **kwargs
):
    if not text_color and not background_color and not bold:
        print(*values, sep, **kwargs)
        return

    background_color_int: Optional[int] = None
    text_color_int: Optional[int] = None

    if background_color:
        if isinstance(background_color, str):
            background_color = _color_hex_to_rgb(background_color)
        background_color_int = _get_minor_distance_color(background_color, colors_dictionary)

    if text_color:
        if isinstance(text_color, str):
            text_color = _color_hex_to_rgb(text_color)
        text_color_int = _get_minor_distance_color(text_color, colors_dictionary)

    print(
        bold_text if bold and not text_color else "",
        (bold_color if bold else txt_color).format(text_color_int) if text_color_int else "",
        bg_color.format(background_color_int) if background_color_int else "",
        sep.join(values),
        reset,
        sep="",
        **kwargs,
    )


def _color_hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
    hex_color = hex_color.replace("#", "")
    if len(hex_color) != 6:
        raise ValueError("The color should be 6 characters long")
    return int(hex_color[:2], 16), int(hex_color[2:4], 16), int(hex_color[4:], 16)


def _color_euclidean_distance(color_a: tuple[int, int, int], color_b: tuple[int, int, int]) -> float:
    distance = 0
    for col_a, col_b in zip(color_a, color_b):
        distance += (col_a - col_b) ** 2
    return sqrt(distance)


def _get_minor_distance_color(selected_color: tuple[int, int, int], colors_dict: dict[str, int]) -> int:
    closest_color = 0
    minor_distance = float("+inf")
    for k, v in colors_dict.items():
        k = tuple(map(int, k.split(",")))
        distance = _color_euclidean_distance(k, selected_color)
        if distance < minor_distance:
            minor_distance = distance
            closest_color = v
    return closest_color


if __name__ == "__main__":
    cprint("This is not bold no color", bold=False)
    cprint("This is bold no color", bold=True)
    cprint("Not bold green text", text_color="#33DD44")
    cprint("Bold green text", text_color="#33DD44", bold=True)
    cprint("Green text pink background", text_color="#33DD44", background_color="#EE4488")
    cprint("Green text bold pink backgroud", text_color="#33DD44", background_color="#EE4488", bold=True)
