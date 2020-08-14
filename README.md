# 👀 csutils - Package for Python 3.8+

This repository contains a collection of handy Python modules to ease some basic tasks like operating on textfiles or to modify colors and cursor position of the Windows terminal. The package is provided as is and may or may not be updated and extended in the future depending on available resources and needs.

## Installation
You can install the package from Github using the following commands from your preferred console. The example below assumes you use [Miniconda](https://docs.conda.io/en/latest/miniconda.html) for managing your Python development environments. So the code may differ, if you use something differnt.

```bash
conda create -n py3env python=3.8
conda activate py3env
conda update pip
pip install git+git://github.com/cwsoft/csutils
```

## Basic usage
```python
from csutils.textparser import Textparser
from csutils.cterm import Colors, Styles, Cursor, Terminal

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

        # Initiate textpareser object with specified textfile.
        tp = Textparser(r"./your_input_file.txt")
        print(tp)

    except KeyboardInterrupt:
        pass

    finally:
        Cursor.enable()
        Terminal.set_style(Styles.RESET)
        print("\nCursor enabled and colors and styles reset to default values.")
```

For details, please have a look into the [API documentation](csutils/docs/) and the examples files in the [docs](csutils/docs/) folder of this repository. To check your system compatibility, you may want to run the unittests provided in the [tests](csutils/tests/) folder.

Have fun 
cwsoft