"""
#######################################################################################
# Module: test_cterm.py
# This module contains some tests for the cterm module.
#
# @package: csutils.cterm
# @author:  cwsoft
# @python:  3.8 or higher
#######################################################################################
"""

import os
import sys

# Monkey patch system path so we can access the csutils package without installing it.
sys.path.append(os.path.abspath(r"../../"))
from csutils.cterm import Colors, Cursor, Styles, Terminal

if __name__ == "__main__":
    try:
        # Initialize terminal (clear screen, set cursor position to row=1, col=1.)
        Terminal.initialize(forecolor=Colors.RESET, backcolor=Colors.RESET)

        # Hide cursor.
        Cursor.disable()
        input("Press ENTER to continue (the cursor is disabled).")

        # Change foreground color to GREEN text with style bold.
        Terminal.set_color(forecolor=Colors.GREEN)
        Terminal.set_style(Styles.BOLD)
        print("Green text with style bold.")

        # Write text to specific position with background color changed (other styles kept).
        Terminal.write(text="POS (row=5, col=10)", row=5, col=10, backcolor=Colors.GREY)
        print("Normal print statement uses last format and position.")

        # Write text to specific position with background color changed (other styles kept).
        Terminal.set_style()
        Terminal.write(
            text="POS (row=4, col=5)",
            row=4,
            col=5,
            styles=(Styles.BOLD, Styles.UNDERLINE),
            auto_reset=True,
        )
        print("Normal print statement called after Terminal.write(auto_reset=True).")

    except KeyboardInterrupt:
        pass

    finally:
        Cursor.enable()
        Terminal.set_style(Styles.RESET)
        print("\nCursor enabled and colors and styles reset to default values.")
