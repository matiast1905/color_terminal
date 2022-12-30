import pickle
import sys
from math import sqrt
from pathlib import Path
from typing import Optional

# Escape sequence
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
background_color = esc + "48;5;{}m"

with open(Path(__file__).parent / "colors_dict.pkl", "rb") as f:
    colors_dictionary = pickle.load(f)


def cprint(
    *values: str,
    text_color: Optional[str | tuple[int, int, int]] = None,
    bg_color: Optional[str | tuple[int, int, int]] = None,
    bold: bool = False,
    sep: str = " ",
    end: str = "\n",
    file=sys.stdout,
    flush: bool = False
) -> None:
    """
    Print the values to a stream, with the possibility of change the text color,
    the background color and text bold.

    Args:
        text_color (Optional[str  |  tuple[int, int, int]], optional):
            Color of the text to print, it could be in hex string format:'#FFFFFF' ;or in RGB tuple
            of int format: (255, 255, 255). Defaults to None.
        bg_color (Optional[str  |  tuple[int, int, int]], optional):
            Color of the text background, it could be in hex string format:'#FFFFFF' ;or in RGB tuple
            of int format: (255, 255, 255). Defaults to None.
        bold (bool, optional): Text in bold format. Defaults to False.
        sep (str, optional): String inserted between values. Defaults to " ".
        end (str, optional): String appended after the last value. Defaults to a newline.
        file (optional): A file-like object (stream). Defaults to the current sys.stdout.
        flush (bool, optional): Whether to forcibly flush the stream. Defaults to False.
    """
    if not text_color and not bg_color and not bold:
        print(*values, sep=sep, end=end, file=file, flush=flush)
        return

    background_color_int: Optional[int] = None
    text_color_int: Optional[int] = None

    if bg_color:
        if isinstance(bg_color, str):
            bg_color = _color_hex_to_rgb(bg_color)
        _validate_rgb_color(bg_color)
        background_color_int = _get_minor_distance_color(bg_color, colors_dictionary)

    if text_color:
        if isinstance(text_color, str):
            text_color = _color_hex_to_rgb(text_color)
        _validate_rgb_color(text_color)
        text_color_int = _get_minor_distance_color(text_color, colors_dictionary)

    print(
        bold_text if bold and not text_color else "",
        (bold_color if bold else txt_color).format(text_color_int) if text_color_int else "",
        background_color.format(background_color_int) if background_color_int else "",
        sep.join(values),
        reset,
        sep="",
        end=end,
        file=file,
        flush=flush,
    )


def _validate_rgb_color(rgb_color: tuple[int, int, int]) -> None:
    """
    Validate that the values of the rgb_color are in the correct range

    Args:
        rgb_color (tuple[int, int, int]): Color in RGB format. ie: (255,255,255)

    Raises:
        ValueError: If color in wrong format
    """
    for value in rgb_color:
        if value < 0 or value > 255:
            raise ValueError("Each RGB color value must be in range 0-255")


def _color_hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
    """
    Helper function that converts a color in hex format '#FFFFFF' to RGB format (255,255,255)

    Args:
        hex_color (str): Color in hex format. ie:'#FFFFFF'

    Raises:
        ValueError: If color in wrong format

    Returns:
        tuple[int, int, int]: Color in RGB format. ie: (255,255,255)
    """
    hex_color = hex_color.replace("#", "")
    if len(hex_color) != 6:
        raise ValueError("The color should be 6 characters long (besides the #)")
    hex_color_list = [hex_color[:2], hex_color[2:4], hex_color[4:]]
    for color in hex_color_list:
        try:
            int(color, 16)
        except ValueError:
            raise ValueError("Each hex color value must be in range 00-FF")
    return tuple(map(lambda x: int(x, 16), hex_color_list))


def _color_euclidean_distance(color_a: tuple[int, int, int], color_b: tuple[int, int, int]) -> float:
    """
    Calculate the euclidean distance between two colors

    Args:
        color_a (tuple[int, int, int]): Color in RGB format. ie: (255,255,255)
        color_b (tuple[int, int, int]): Color in RGB format. ie: (255,255,255)

    Returns:
        float: Euclidean distance between the two colors
    """
    distance: float = 0.0
    for col_a, col_b in zip(color_a, color_b):
        distance += (col_a - col_b) ** 2
    return sqrt(distance)


def _get_minor_distance_color(selected_color: tuple[int, int, int], colors_dict: dict[str, int]) -> int:
    """
    Returns the code of the closest color to that selected by the user

    Args:
        selected_color (tuple[int, int, int]): Color in RGB format. ie: (255, 255, 255)
        colors_dict (dict[str, int]): Map of color in RGB format and it's color code

    Returns:
        int: Code of the selected color
    """
    closest_color = 0
    minor_distance = float("+inf")
    for k, v in colors_dict.items():
        k = tuple(map(int, k.split(",")))
        distance = _color_euclidean_distance(k, selected_color)
        if distance < minor_distance:
            minor_distance = distance
            closest_color = v
    return closest_color
