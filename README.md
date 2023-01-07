# Colorise Terminal

This package allows you to change the text color, background color and bold of the terminal output.

To use it, you only need to import one function

`from colorise_terminal import cprint`

`cprint` have the same parameters than the regular `print` functions, but adds 3 more: *text_color*, *bg_color* and *bold*


- text_color:
    Color of the text to print, it could be in hex string format: **'#FFAA00'** ; or in RGB tuple
    of integer format: **(255, 170, 0)**. Defaults to None.

- bg_color :
    Color of the text background, it could be in hex string format:**'#22CC33'** ;or in RGB tuple
    of integer format: **(34, 204, 51)**. Defaults to None.

- bold (bool): Text in bold format. Defaults to False.

These are all optional paramaters, so if you omit all of them `cprint` will behave as regular `print`.

Here are some examples of the function working in a terminal session:

![test](https://github.com/matiast1905/colorise_terminal/blob/main/images/colorise_terminal_test.png?raw=true)
