import re

from src.globals_vars import (
    OPERATORS,
    SIGN,
    COMMA,
    OPEN_PARENTHESES,
    CLOSING_PARENTHESES,
    MATRICE_CLOSING_PARENTHESES,
    MATRICE_OPEN_PARENTHESES,
    MATRICE_LINE_SEPARATOR,
    MATRICE_COLUMN_SEPARATOR,
)

regex_potential_matrice = re.compile(
    rf"\{MATRICE_OPEN_PARENTHESES}.*\{MATRICE_CLOSING_PARENTHESES}"
)
regex_matrice_column = re.compile(
    rf"\{MATRICE_OPEN_PARENTHESES}(.*?)\{MATRICE_CLOSING_PARENTHESES}"
)
regex_comma = f"\{COMMA}"
regex_functions = re.compile(rf"[A-Z]+\([\d{regex_comma}iA-Z]+\)")
regex_variables = re.compile(r"[A-Z]+")
regex_function_name = re.compile(r"[A-Z]+")
regex_function_argument = re.compile(rf"(?<=\()[A-Z\di{regex_comma}]+(?=\))")
regex_complex = re.compile(rf"(i)")
regex_real = re.compile(rf"(\d+{regex_comma}*\d+(?!{regex_comma}))|(\d+(?!{regex_comma}))")
regex_var = (
    "\="
    + "\?"
    + "\\"
    + "\\".join(OPERATORS)
    + "\\"
    + "\\".join(SIGN)
    + "\\"
    + "\\".join(OPEN_PARENTHESES)
    + "\\"
    + "\\".join(CLOSING_PARENTHESES)
)
regex_operators = re.compile(rf"[{regex_var}]")

allowed_char_list = (
    "\="
    + "\?"
    + "\\"
    + "\\".join(OPERATORS)
    + "\\"
    + "\\".join(SIGN)
    + "\\"
    + "\\".join(OPEN_PARENTHESES)
    + "\\"
    + "\\".join(CLOSING_PARENTHESES)
    + "\\"
    + "\\".join(COMMA)
    + "\\"
    + "\\".join(MATRICE_OPEN_PARENTHESES)
    + "\\"
    + "\\".join(MATRICE_CLOSING_PARENTHESES)
    + "\\"
    + "\\".join(MATRICE_LINE_SEPARATOR)
    + "\\"
    + "\\".join(MATRICE_COLUMN_SEPARATOR)
)
regex_check_forbidden_char = re.compile(pattern=rf"[^\d\w{allowed_char_list}]")
