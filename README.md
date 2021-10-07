# ComputorV2 [(subject)](https://cdn.intra.42.fr/pdf/pdf/5667/en.pdf)

![gif](computorv2.gif)

A calculator interpreter than can operate on real, complex numbers, and 2D matrix data types, store variables, define and evaluate functions, and solve quadratic equations in Python.

Improvement of [computorv1](https://github.com/Sithi5/computorv1).

## How to install

Create a virtual environment and activate it
```bash
python -m venv venv
.\venv\Scripts\activate.bat # on Windows
```

Install the pre-requirement:
```bash
pip install -U -r pre-requirements.txt
```

Execute `setup.py`:

* for dev:
```bash
pip install --editable .[dev]
```
* For user:
```bash
pip install .
```

## How to run

Launch `computorv2`:

```bash
computorv2 --help

usage: computorv2 [-h] [--gui] [-e EXPRESSION] [-v] [-vv] [-d] [--output_graph]

optional arguments:
  -h, --help            show this help message and exit
  --gui                 Launch computor in GUI mode
  -e EXPRESSION, --expression EXPRESSION
                        Insert expression to resolve. Insert 'shell' if you want inline shell expression resolver.
  -v, --verbose         Add verbose and print different resolving step.
  -vv, --force_calculator_verbose
                        Add all verbose and force the calculator verbose.
  -d, --debug           Remove exception catching.
  --output_graph        In case there is a possible graph to create, it will output it in a new file.
```

## How to test

```bash
pytest .\tests
```

## Resources
* [https://mathworld.wolfram.com/ComplexDivision.html](https://mathworld.wolfram.com/ComplexDivision.html)
* [https://www.mathsisfun.com/numbers/complex-numbers.html](https://www.mathsisfun.com/numbers/complex-numbers.html)
* [https://www.expii.com/t/exponential-form-of-a-complex-number-9210](https://www.expii.com/t/exponential-form-of-a-complex-number-9210)