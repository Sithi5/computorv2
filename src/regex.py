import re

from src.globals_vars import (
    EQUALS_SIGN,
    QUESTIONS_SIGN,
    OPERATORS,
    SIGN,
    COMMA,
    OPEN_PARENTHESES,
    CLOSING_PARENTHESES,
    MATRICE_CLOSING_PARENTHESES,
    MATRICE_OPEN_PARENTHESES,
    MATRICE_ROW_SEPARATOR,
    MATRICE_COLUMN_SEPARATOR,
    MATRIX_MULTIPLICATION_SIGN,
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


operators_string = "\\" + "\\".join(OPERATORS) + "\\" + "\\".join(SIGN)
parenthesis_string = "\\" + "\\".join(OPEN_PARENTHESES) + "\\" + "\\".join(CLOSING_PARENTHESES)
operators_parenthesis_string = operators_string + parenthesis_string
operators_parenthesis_equal_question_string = (
    "\\"
    + "\\".join(EQUALS_SIGN)
    + "\\"
    + "\\".join(QUESTIONS_SIGN)
    + "\\"
    + operators_parenthesis_string
    + "\\"
    + "\\".join(MATRIX_MULTIPLICATION_SIGN)
)
regex_operators_parenthesis_equal_question = re.compile(
    rf"[{operators_parenthesis_equal_question_string}]"
)

regex_operators_parenthesis = re.compile(rf"[{operators_parenthesis_string}]")

allowed_char_string = (
    "\\"
    + "\\".join(EQUALS_SIGN)
    + "\\"
    + "\\".join(QUESTIONS_SIGN)
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
    + "\\".join(MATRICE_ROW_SEPARATOR)
    + "\\"
    + "\\".join(MATRICE_COLUMN_SEPARATOR)
    + "\\"
    + "\\".join(MATRIX_MULTIPLICATION_SIGN)
)
regex_check_forbidden_char = re.compile(pattern=rf"[^\d\w{allowed_char_string}]")


def matching_first_potential_matrice(string: str) -> str:
    """
    Try to match a matrix from the start of the expression and return it as an str match.
    Return None if no match found.
    Matching example : '[[5,5];[4,4]] + [[7,5];[3,3]]' => '[[5,5];[4,4]]'
    This functions does not parse the inside of the matrix.
    For example: '[[5,,,3];;[123]]' will be returned as a potential matrix.
    """
    # First char should be an open matrice parenthesis.
    if string[0] != MATRICE_OPEN_PARENTHESES:
        return None
    matched_string: str = "["
    open_parentheses_count = 1
    for char in string[1:]:
        if char == MATRICE_OPEN_PARENTHESES:
            open_parentheses_count += 1
        elif char == MATRICE_CLOSING_PARENTHESES:
            open_parentheses_count -= 1
        matched_string += char
        if open_parentheses_count == 0:
            return matched_string
    return None
