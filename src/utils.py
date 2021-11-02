# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    utils.py                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: mabouce <ma.sithis@gmail.com>              +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/12/03 18:10:41 by mabouce           #+#    #+#              #
#    Updated: 2021/07/25 12:48:58 by mabouce          ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from src.globals_vars import *

from src.math_utils import is_real


def split_expression_parts_from_tokens(tokens: list):
    """
    This function split a tokenized expression in two part.
    The left and the right part respectively splitted from the '=' operator.
    The input tokens list should be in the format of : '...' + '=' + '...'.
    """
    add_to_left_part = True
    left_part: list = []
    right_part: list = []
    for token in tokens:
        if token != "=" and add_to_left_part is True:
            left_part.append(token)
        elif token != "=" and add_to_left_part is False:
            right_part.append(token)
        elif token == "=":
            add_to_left_part = False
    if len(left_part) == 0 or len(right_part) == 0:
        raise SyntaxError("The equation is not well formated. No left or right part.")
    else:
        return (left_part, right_part)


def convert_expression_to_upper(input_string: str) -> str:
    """
    Convert every alpha char into uppercase except isolated I/i char that will be converted to lowercase because it is imaginary numbers."""
    converted_string = ""
    for index, c in enumerate(input_string):
        if (
            c.lower() == "i"
            and (index == 0 or not input_string[index - 1].isalpha())
            and (index + 1 == len(input_string) or not input_string[index + 1].isalpha())
        ):
            converted_string = converted_string + c.lower()
        elif c.isalpha():
            converted_string = converted_string + c.upper()
        else:
            converted_string = converted_string + c

    return converted_string


def convert_signed_number(expression: str, accept_var: bool = False):
    """
    This function convert signed number in a string to a sentence readable for npi process.
    Exemple :
        5 * -5 is converted to 5 * (0 - 5)
        10 / +5 is converted to 10 / (0 + 5)
    """
    if len(expression) > 1:
        if expression[0] in SIGN and (
            is_real(expression[1])
            or expression[1] in OPEN_PARENTHESES
            or (expression[1].isalpha() and accept_var)
        ):
            # Convert first sign : expression = "-5 + 2" --> "(0 - 5) + 2"
            i = 1
            number = ""
            if expression[i] in OPEN_PARENTHESES:
                while i < len(expression) and (expression[i] not in CLOSING_PARENTHESES):
                    number = number + expression[i]
                    i += 1
            else:
                while i < len(expression) and (is_real(expression[i]) or expression[i] in COMMA):
                    number = number + expression[i]
                    i += 1
            if len(number) > 0:
                expression = "(0" + expression[0] + number + ")" + expression[i:]
            elif accept_var:
                i = 1
                var_name = ""
                while i < len(expression) and expression[i].isalpha():
                    var_name = var_name + expression[i]
                    i += 1
                if len(var_name) > 0:
                    expression = "(0" + expression[0] + var_name + ")" + expression[i:]

        for operator in OPERATORS + OPEN_PARENTHESES + MATRICE_OPEN_PARENTHESES + "=":
            for sign in SIGN:
                split = expression.split(operator + sign)
                if len(split) > 1:
                    # Starting with 2nd part
                    index = 1
                    while index < len(split):
                        # Getting number
                        number = ""
                        i = 0
                        while i < len(split[index]):
                            if not is_real(split[index][i]) and not split[index][i] in COMMA:
                                break
                            number = number + split[index][i]
                            i += 1
                        # Replacing signed number by the new sentence
                        if len(number) > 0:
                            split[index] = operator + "(0" + sign + number + ")" + split[index][i:]
                        # If no number, maybe it's a var:
                        elif accept_var:
                            # Getting varname
                            var_name = ""
                            i = 0
                            while i < len(split[index]):
                                if not split[index][i].isalpha():
                                    break
                                var_name = var_name + split[index][i]
                                i += 1
                            if len(var_name) > 0:
                                split[index] = (
                                    operator + "(0" + sign + var_name + ")" + split[index][i:]
                                )
                            else:
                                split[index] = operator + sign + split[index][i:]
                        else:
                            split[index] = operator + sign + split[index][i:]
                        index += 1

                expression = "".join(split)
    return expression


def add_implicit_cross_operator_for_vars(vars_list: list, expression: str):
    """
    This function take a string expression and add implicit multiplier for variables.
        Exemple :
        5X -> 5 * X
        X(5+2) -> X*(5+2)
    """
    # Splitting from vars
    for var in vars_list:
        splitted_expression = expression.split(var)
        index = 1
        while index < len(splitted_expression):
            # Checking if previous part is not empty
            if len(splitted_expression[index - 1]) > 0:
                # Getting previous part to check sign
                if (
                    splitted_expression[index - 1][-1].isdecimal() is True
                    or splitted_expression[index - 1][-1] in CLOSING_PARENTHESES
                ):
                    splitted_expression[index - 1] = splitted_expression[index - 1] + "*"
            # Checking implicit mult after the var
            if splitted_expression[index] and (
                splitted_expression[index][0].isdecimal() is True
                or splitted_expression[index][0] in OPEN_PARENTHESES
            ):
                splitted_expression[index] = "*" + splitted_expression[index]
            index += 1
        expression = var.join(splitted_expression)
    return expression


def parse_sign(expression: str):
    """
    Removing extra _sign
    """
    while (
        SUBSTRACTION_SIGN + SUBSTRACTION_SIGN in expression
        or ADDITION_SIGN + ADDITION_SIGN in expression
        or SUBSTRACTION_SIGN + ADDITION_SIGN in expression
        or ADDITION_SIGN + SUBSTRACTION_SIGN in expression
    ):
        expression = (
            expression.replace(SUBSTRACTION_SIGN + SUBSTRACTION_SIGN, ADDITION_SIGN)
            .replace(ADDITION_SIGN + ADDITION_SIGN, ADDITION_SIGN)
            .replace(ADDITION_SIGN + SUBSTRACTION_SIGN, SUBSTRACTION_SIGN)
            .replace(SUBSTRACTION_SIGN + ADDITION_SIGN, SUBSTRACTION_SIGN)
        )
    if len(expression) > 0:
        if expression[0] == ADDITION_SIGN:
            expression = expression[1:]
    return expression


def get_var_multiplier(var, var_name) -> float:
    # Cutting power
    var = var.split("^")[0]
    # Removing varname
    var = var.replace(var_name, "")
    # Removing extra mult operator
    var = var.replace("*", "")

    # This is because we can have X or -X
    if var == SUBSTRACTION_SIGN:
        var = -1
    elif len(var) < 1:
        var = 1
    return float(var)
