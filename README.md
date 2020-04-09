# 👀 csutils - Package for Python 3.6+

This repository contains a collection of handy Python modules to ease some basic tasks like operating on textfiles. The package is provided as is and may or may not be updated and extended in the future depending on available resources and needs.

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

tp = Textparser(r"./your_input_textfile")
print(tp)
```

For a detailed introduction please check out the examples provided in the [tests](csutils/tests/) folder of this repository.


Have fun 
cwsoft