import re

from src.types.types import *

from globals_vars import (
    OPERATORS,
    SIGN,
    COMMA,
    OPEN_PARENTHESES,
    CLOSING_PARENTHESES,
    MATRICE_CLOSING_PARENTHESES,
    MATRICE_OPEN_PARENTHESES,
)


def convert_expression_to_type_list(expression: str) -> list:
    type_list: list = []
    regex_potential_matrice = re.compile(
        rf"\{MATRICE_OPEN_PARENTHESES}.*{MATRICE_CLOSING_PARENTHESES}]"
    )
    regex_var = f"\{COMMA}"
    regex_functions = re.compile(rf"[A-Z]+\([\d{regex_var}A-Z]+\)")
    regex_variables = re.compile(r"[A-Z]+")
    regex_var = f"\{COMMA}"
    regex_complex = re.compile(rf"(\d+{regex_var}*\d+i)|(\d+i)")
    regex_var = f"\{COMMA}"
    regex_real = re.compile(rf"(\d+{regex_var}*\d+(?!{regex_var}))|(\d+(?!{regex_var}))")
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
    while expression != "":
        match_size = 0
        matched_potential_matrice = regex_potential_matrice.match(string=expression)
        matched_function = regex_functions.match(string=expression)
        matched_variable = regex_variables.match(string=expression)
        matched_operator = regex_operators.match(string=expression)
        matched_complex = regex_complex.match(string=expression)
        matched_real = regex_real.match(string=expression)

        # matching matrice should be first because it can be compound of more matrice/real/var etc.
        if matched_potential_matrice:
            match_size = len(matched_potential_matrice.group(0))
            type_list.append(Matrice(value=matched_potential_matrice.group(0)))
            print(
                "matched_potential_matrice = ",
                matched_potential_matrice.group(0),
            )
        # Match functions before var because can have a var inside
        elif matched_function:
            match_size = len(matched_function.group(0))
            print(
                "matched_function = ",
                matched_function.group(0),
            )
        # Find variables
        elif matched_variable:
            print(
                "matched_variable = ",
                matched_variable.group(0),
            )
            match_size = len(matched_variable.group(0))
        elif matched_operator:
            type_list.append(Operator(value=matched_operator.group(0)))
            print(
                "matched_operator = ",
                matched_operator.group(0),
            )
            match_size = len(matched_operator.group(0))
        # Match complex before numbers
        elif matched_complex:
            type_list.append(Complex(value=matched_complex.group(0)))
            print(
                "matched_complex = ",
                matched_complex.group(0),
            )
            match_size = len(matched_complex.group(0))
        elif matched_real:
            type_list.append(Real(value=matched_real.group(0)))
            print(
                "matched_real = ",
                matched_real.group(0),
            )
            match_size = len(matched_real.group(0))
        else:
            raise SyntaxError("Some numbers are not well formated : " + expression)

        expression = expression[match_size:]
    print("type_list = ", type_list)
    return type_list