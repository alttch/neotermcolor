# neotermcolor
#
# Copyright (c) 2019 Altertech (https://www.altertech.com)
# Author: Sergei S. (https://www.makeitwork.cz/)

# Termcolor original
# Copyright (c) 2008-2011 Volvox Development Team
#
# Author: Konstantin Lepa <konstantin.lepa@gmail.com>
#
# License: MIT
"""ANSII Color formatting for output in terminal."""

import os
import sys
import platform

VERSION = (2, 0, 7)

__version__ = '2.0.7'

ATTRIBUTES = dict(
    list(
        zip([
            'bold', 'dark', '', 'underline', 'blink', '', 'reverse', 'concealed'
        ], list(range(1, 9)))))
del ATTRIBUTES['']

HIGHLIGHTS = dict(
    list(
        zip([
            'on_grey', 'on_red', 'on_green', 'on_yellow', 'on_blue',
            'on_magenta', 'on_cyan', 'on_white'
        ], list(range(40, 48)))))

COLORS = dict(
    list(
        zip([
            'grey',
            'red',
            'green',
            'yellow',
            'blue',
            'magenta',
            'cyan',
            'white',
        ], list(range(30, 38)))))

PALETTE = {}

STYLES = {}

RESET = '\033[0m'
'''
If true, text is not colored if stdout/stderr is not a TTY
'''
tty_aware = True
readline_always_safe = False

_isatty = sys.stdout.isatty() and sys.stderr.isatty()


def set_color(name, code):
    '''
    Set (override) color

    Args:
        name: color name (e.g. 'red')
        code: color code (e.g. 196)
    '''
    PALETTE[name] = code


def set_style(name, color=None, on_color=None, attrs=None):
    '''
    Define a style

    Args:
        color: text color
        on_color: highlights color
        attrs: additional attributes
    '''
    if isinstance(name, str) and name.startswith('@'):
        name = name[1:]
    STYLES[name] = (color, on_color, attrs)


def colored(text,
            color=None,
            on_color=None,
            attrs=None,
            style=None,
            readline_safe=False):
    """Colorize text.

    Available text colors:
        red, green, yellow, blue, magenta, cyan, white.

    Available text highlights:
        on_red, on_green, on_yellow, on_blue, on_magenta, on_cyan, on_white.

    Available attributes:
        normal, bold, dark, underline, blink, reverse, concealed.

    Example:
        colored('Hello, World!', 'red', 'on_grey', ['blue', 'blink'])
        colored('Hello, World!', 'green')

    Args:
        text: text to colorize
        color: text color
        on_color: highlights color
        attrs: additional attributes
        style: pre-defined style (you may also choose style as color='@NAME')
        readline_safe: if True, additional escape codes are used to avoid
                       problems with readline library
    """
    text = str(text)
    if os.getenv('ANSI_COLORS_DISABLED') is None and (not tty_aware or _isatty):

        fmt_str = '{}{}m'

        if readline_safe or readline_always_safe:
            fmt_str = '\001' + fmt_str + '\002'

        fmt_str += '{}'

        if isinstance(color, str) and color.startswith('@'):
            style = color[1:]
            color = None

        if style is not None:
            c, o, a = STYLES[style[1:] if \
                    isinstance(style, str) and style.startswith('@') else style]
            if color is None:
                color = c
            if on_color is None:
                on_color = o
            if attrs is None:
                attrs = a

        if color is not None:

            if color in PALETTE:
                color = PALETTE[color]

            if isinstance(color, str):
                c = COLORS[color]
                ESC = '\033['
            else:
                c = color
                ESC = '\x1b[38;5;'

            text = fmt_str.format(ESC, c, text)

        if on_color is not None:

            if on_color in PALETTE:
                on_color = PALETTE[on_color]

            if isinstance(on_color, str):
                c = HIGHLIGHTS[on_color]
                ESC = '\033['
            else:
                c = on_color
                ESC = '\x1b[48;5;'

            text = fmt_str.format(ESC, c, text)

        if attrs is not None:
            for attr in [attrs] if isinstance(attrs, str) else attrs:
                if attr != '' and attr != 'normal':
                    text = fmt_str.format('\033[', ATTRIBUTES[attr], text)

        if readline_safe or readline_always_safe:
            text += '\001' + RESET + '\002'
        else:
            text += RESET
    return text


def cprint(text,
           color=None,
           on_color=None,
           attrs=None,
           style=None,
           readline_safe=False,
           **kwargs):
    """Print colorize text.

    It accepts arguments of print function.
    """

    print((colored(text, color, on_color, attrs, style, readline_safe)),
          **kwargs)


def test():
    print('Current terminal type: %s' % os.getenv('TERM'))
    print('Test basic colors:')
    cprint('Grey color', 'grey')
    cprint('Red color', 'red')
    cprint('Green color', 'green')
    cprint('Yellow color', 'yellow')
    cprint('Blue color', 'blue')
    cprint('Magenta color', 'magenta')
    cprint('Cyan color', 'cyan')
    cprint('White color', 'white')
    print(('-' * 78))

    print('Test highlights:')
    cprint('On grey color', on_color='on_grey')
    cprint('On red color', on_color='on_red')
    cprint('On green color', on_color='on_green')
    cprint('On yellow color', on_color='on_yellow')
    cprint('On blue color', on_color='on_blue')
    cprint('On magenta color', on_color='on_magenta')
    cprint('On cyan color', on_color='on_cyan')
    cprint('On white color', color='grey', on_color='on_white')
    print('-' * 78)

    print('Test attributes:')
    cprint('Bold grey color', 'grey', attrs=['bold'])
    cprint('Dark red color', 'red', attrs=['dark'])
    cprint('Underline green color', 'green', attrs=['underline'])
    cprint('Blink yellow color', 'yellow', attrs=['blink'])
    cprint('Reversed blue color', 'blue', attrs=['reverse'])
    cprint('Concealed Magenta color', 'magenta', attrs=['concealed'])
    cprint('Bold underline reverse cyan color',
           'cyan',
           attrs=['bold', 'underline', 'reverse'])
    cprint('Dark blink concealed white color',
           'white',
           attrs=['dark', 'blink', 'concealed'])
    print(('-' * 78))

    print('Test mixing:')
    cprint('Underline red bold on grey color', 'red', 'on_grey',
           ['underline', 'bold'])
    cprint('Reversed green on red color', 'green', 'on_red', ['reverse'])
    print(('-' * 78))

    print('256-color palette')
    for c in range(0, 256):
        cprint('{:03d} '.format(c), color=c, end='')
    print()
    for c in range(0, 256):
        cprint('{:03d} '.format(c), on_color=c, end='')
    print()
    print(('-' * 78))
    print('Test 256-color mixing:')
    cprint('Underline light-green (119) on grey (237)', 119, 237, 'underline')
    cprint('Reversed dark magenta(90) on purple (197), blinking', 90, 197,
           ['reverse', 'blink'])
    print(('-' * 78))
    print('Test palette')
    set_color('red', 197)
    cprint('Red color is now purple', 'red')
    print(('-' * 78))
    print('Test styles')
    set_style('warning', color=208, attrs='bold')
    cprint('WARNING TEXT', color='@warning')
    set_style('error', color='red', attrs='bold')
    cprint('ERROR TEXT', style='error')
    set_style('info', color=157)
    # test style overriding and '@' in style (wrong but should work)
    cprint('INFO TEXT', color='white', style='@info')


if platform.system().lower() == 'windows':
    from ctypes import windll, c_int, byref, c_void_p
    ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004
    INVALID_HANDLE_VALUE = c_void_p(-1).value
    STD_OUTPUT_HANDLE = c_int(-11)
    hStdout = windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
    if hStdout != INVALID_HANDLE_VALUE:
        mode = c_int(0)
        if windll.kernel32.GetConsoleMode(c_int(hStdout), byref(mode)):
            mode = c_int(mode.value | ENABLE_VIRTUAL_TERMINAL_PROCESSING)
            windll.kernel32.SetConsoleMode(c_int(hStdout), mode)

if __name__ == '__main__':
    test()
