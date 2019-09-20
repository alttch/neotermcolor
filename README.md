# modern ANSII Color formatting for output in terminal

## What is neotermcolor

neotermcolor library is a fork of old good
[termcolor](https://pypi.org/project/termcolor/), which is widely used. I like
it very much, but unfortunately last release was long time ago.

Everything is fully backward compatible with original termcolor:

```python
import sys
from neotermcolor import colored, cprint

text = colored('Hello, World!', 'red', attrs=['reverse', 'blink'])
print(text)
cprint('Hello, World!', 'green', 'on_red')

print_red_on_cyan = lambda x: cprint(x, 'red', 'on_cyan')
print_red_on_cyan('Hello, World!')
print_red_on_cyan('Hello, Universe!')

for i in range(10):
    cprint(i, 'magenta', end=' ')

cprint("Attention!", 'red', attrs=['bold'], file=sys.stderr)
```

## Installation

```shell
    pip3 install neotermcolor
```

## New features

### It works in Windows terminal

Yep, right out-of-the-box (tested on Windows 10)

### It is readline-safe

When you mix ANSI color codes with readline input, it may cause a problem.
neotermcolor has a workaround:

* new param for **cprint** and **colored**: *readline_safe=True*
* you may also turn on readline-safe colorizing by default, setting

```python
    import neotermcolor

    neotermcolor.readline_always_safe = True
```

### It has 256-color palette

If color code is specified as an integer (0..255), ANSI 256-color palette is
used. You may specify color codes both for foreground and background and mix
them with other attributes:

```python
    from neotermcolor import cprint

    cprint('Underline light-green (119) on grey (237)', 119, 237, ['underline'])
```

### It is TTY-aware

neotermcolor will not colorize text if process stdout or stderr is not a TTY.

This feature is on by default, but you may turn it off:

```python
    import neotermcolor

    neotermcolor.tty_aware = False
```

### It has palette overriding

You may define own color names or override existing ones: e.g. you may use
standard palette for 16-color terminals, but override it when your program
detect terminal with 256-color support or when it's forced by user:

```python
    import neotermcolor

    neotermcolor.set_color('red', 197)
    neotermcolor.cprint('Red color is now purple', 'red')
```

### It has styles

Styles are alternative to classical defining a "style" for certain type of
messages with *functools.partial* or *lambda*. A style may contain color,
on_color and attributes:

```python
    import neotermcolor

    neotermcolor.set_style('error', color='red', attrs='bold')
    neotermcolor.cprint('ERROR MESSAGE', style='error')
    # or
    neotermcolor.cprint('ERROR MESSAGE 2', '@error')
```

Note: if you specify both style and e.g. attrs, the style attrs will be
overriden.

### Single attribute can now be specified as a string

```python
    # as list or tuple
    cprint('test', attrs=['bold'])
    # as a string
    cprint('test', attrs='bold')
```

### How to use it instead of old termcolor in the existing projects

```python
    import neotermcolor as termcolor
```

I'll do my best to keep it backward compatible with original termcolor.

Enjoy!
