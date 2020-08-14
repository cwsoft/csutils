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

        # Change foreground color to GREEN and text style to bold and underline.
        Terminal.set_color(forecolor=Colors.GREEN)
        Terminal.set_style(Styles.BOLD, Styles.UNDERLINE)
        print("All text outputs below are green, bold and underline.")

    except KeyboardInterrupt:
        pass

    finally:
        Cursor.enable()
        Terminal.set_style(Styles.RESET)
        print("\nCursor enabled and colors and styles reset to default values.")