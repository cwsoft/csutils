"""
#######################################################################################
# Module for basic terminal color and cursor manipulations via an easy to use API.
# Under the hood ANSI escape sequences are printed to stdout of the terminal.
#
# Some details about ANSI escape sequences can be found here:
# - https://de.wikipedia.org/wiki/ANSI-Escapesequenz
# - https://docs.microsoft.com/en-us/windows/console/console-virtual-terminal-sequences
#
# @module:    cterm
# @platform:  Windows 10
# @author:    cwsoft
# @python:    3.8 or higher
#######################################################################################
"""

from enum import Enum

__version__ = "1.1.0"


class Ansi(Enum):
    """Basic ANSI control sequences."""

    CSI = "\033["  # Control Sequence Intro
    OSC = "\033]"  # Operating System Command (not yet used)


class Colors(Enum):
    """Basic terminal foreground color codes. For background colors simply increment by 10."""

    BLACK = 30
    RED = 31
    GREEN = 32
    YELLOW = 33
    BLUE = 34
    MAGENTA = 35
    CYAN = 36
    WHITE = 37
    RESET = 39
    GREY = 90
    BRIGHT_RED = 91
    BRIGHT_GREEN = 92
    BRIGHT_YELLOW = 93
    BRIGHT_BLUE = 94
    BRIGHT_MAGENTA = 95
    BRIGHT_CYAN = 96
    BRIGHT_WHITE = 97


class Styles(Enum):
    """Basic terminal styles supported by most terminals."""

    RESET = 0
    BOLD = 1
    UNDERLINE = 4
    REVERSE = 7


class Cursor:
    """Static class allowing basic cursor operations supported by most terminals."""

    @staticmethod
    def disable():
        """Disable (hide) terminal cursor."""
        print(f"{Ansi.CSI.value}?25l", end="")

    @staticmethod
    def enable():
        """Enables (show) terminal cursor."""
        print(f"{Ansi.CSI.value}?25h", end="")

    @staticmethod
    def store_pos():
        """Store actual cursor position in memory."""
        print(f"{Ansi.CSI.value}s", end="")

    @staticmethod
    def restore_pos():
        """Restore cursor position from last stored position in memory."""
        print(f"{Ansi.CSI.value}u", end="")

    @staticmethod
    def set_pos(row=1, col=1):
        """Set cursor position to specified terminal row, col coordinates."""
        print(f"{Ansi.CSI.value}{row};{col}f", end="")

    @staticmethod
    def up(pos=1):
        """Move cursor up by pos rows."""
        print(f"{Ansi.CSI.value}{pos}A", end="")

    @staticmethod
    def down(pos=1):
        """Move cursor down by pos rows."""
        print(f"{Ansi.CSI.value}{pos}B", end="")

    @staticmethod
    def right(pos=1):
        """Move cursor to the right by pos cols (assuming LTR languages)."""
        print(f"{Ansi.CSI.value}{pos}C", end="")

    @staticmethod
    def left(pos=1):
        """Move cursor to the left by n-cols (assuming LTR languages)."""
        print(f"{Ansi.CSI.value}{pos}D", end="")


class Terminal:
    """Static class to modify terminal colors and cursor position and output formated text."""

    class Clear(Enum):
        """Supported clear modes used in the terminal clear methods."""

        POS_TO_END = 0
        BEGINN_TO_POS = 1
        ALL = 2

    @staticmethod
    def initialize(forecolor=Colors.RESET, backcolor=Colors.RESET):
        """Initialize terminal window (reset colors, clear output, set cursor to top-left position."""
        Terminal.set_color(forecolor, backcolor)
        Terminal.clear(mode=Terminal.Clear.ALL)
        Cursor.set_pos(row=1, col=1)

    @staticmethod
    def clear(mode=Clear.ALL):
        """Clear terminal screen. Mode must be of Enum Terminal.Clear."""
        assert isinstance(mode, Terminal.Clear), "Param 'mode' must be of Enum Terminal.Clear."
        print(f"{Ansi.CSI.value}{mode.value}J")

    @staticmethod
    def clear_line(mode=Clear.ALL):
        """Clear terminal screen. Mode must be of Enum Terminal.Clear."""
        assert isinstance(mode, Terminal.Clear), "Param 'mode' must be of Enum Terminal.Clear."
        print(f"{Ansi.CSI.value}{mode.value}M")

    @staticmethod
    def set_color(forecolor=None, backcolor=None):
        """Set terminal fore- and background color to specified values. Colors must be of Enum Colors.
        Example: set_color(forecolor=Colors.RED, backcolor=Colors.YELLOW)."""
        if not forecolor is None:
            assert isinstance(forecolor, Colors), "Param 'forecolor' must be of Enum cterm.Colors."
            print(f"{Ansi.CSI.value}{forecolor.value}m", end="")

        if not backcolor is None:
            assert isinstance(backcolor, Colors), "Param 'backcolor' must be of Enum cterm.Colors."
            print(f"{Ansi.CSI.value}{int(backcolor.value) + 10}m", end="")

    @staticmethod
    def set_style(*styles):
        """Set terminal font styles to specified values. Font styles must be of Enum Styles.
        Example: set_style(Styles.BOLD, Styles.UNDERLINE)."""
        # Reset styles if no style was defined.
        if not styles:
            print(f"{Ansi.CSI.value}{Styles.RESET.value}m", end="")
            return

        # Loop through style enum args and apply all styles in sequence.
        for style in styles:
            assert isinstance(style, Styles), "Param(s) 'styles' must be of Enum cterm.Styles."
            print(f"{Ansi.CSI.value}{style.value}m", end="")

    @staticmethod
    def write(text, row=None, col=None, forecolor=None, backcolor=None, styles=None, auto_reset=False):
        """Writes text to specified position with specified colors and styles. By default no line end is added.
        Note: styles can be a single Enum cterm.Styles or a collection of Enum cterm.Styles."""
        if auto_reset:
            Cursor.store_pos()

        # Set row and col position if specified.
        if isinstance(row, int) and isinstance(col, int):
            Cursor.set_pos(max(1, row), max(1, col))

        # Set terminal colors if specified.
        Terminal.set_color(forecolor, backcolor)

        # Set font styles if specified.
        if isinstance(styles, Styles):
            Terminal.set_style(styles)
        elif isinstance(styles, (list, tuple)):
            Terminal.set_style(*styles)

        # Write text to terminal using optional position, colors and styles.
        print(text, end="")

        # Reset colors, styles and cursor position if auto_reset is set.
        if auto_reset:
            Terminal.set_color(forecolor=Colors.RESET, backcolor=Colors.RESET)
            Terminal.set_style(Styles.RESET)
            Cursor.restore_pos()
