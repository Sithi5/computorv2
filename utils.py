# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    utils.py                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: mabouce <ma.sithis@gmail.com>              +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/12/03 18:10:41 by mabouce           #+#    #+#              #
#    Updated: 2021/07/15 19:10:46 by mabouce          ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from globals_vars import (
    _OPERATORS,
    _SIGN,
    _COMMA,
    _OPEN_PARENTHESES,
    _CLOSING_PARENTHESES,
)


def is_number(n: str) -> bool:
    try:
        float(n)
        return True
    except ValueError:
        return False


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


def convert_to_tokens(expression: str) -> list:
    """
    Convert a string expression into tokens.
    Numbers and var name will stay in a single token.
    """
    tokens = []
    current_char = 0
    last_char = 0
    while current_char < len(expression):
        # Getting full number
        if is_number(expression[current_char]):
            while current_char < len(expression) and (
                is_number(expression[current_char]) or expression[current_char] in _COMMA
            ):
                current_char += 1
        # Getting full var name
        elif expression[current_char].isalpha():
            while current_char < len(expression) and (expression[current_char].isalpha()):
                current_char += 1
        else:
            current_char += 1
        tokens.append(expression[last_char:current_char])
        last_char = current_char
    return tokens


def convert_signed_number(expression: str, accept_var: bool = False):
    """
    This function convert signed number in a string to a sentence readable for npi process.
    Exemple :
        5 * -5 is converted to 5 * (0 - 5)
        10 / +5 is converted to 10 / (0 + 5)
    """
    # Checking for first sign
    if len(expression) > 1:
        if expression[0] in _SIGN and (
            is_number(expression[1])
            or expression[1] in _OPEN_PARENTHESES
            or (expression[1].isalpha() and accept_var)
        ):
            i = 1
            number = ""
            if expression[i] in _OPEN_PARENTHESES:
                while i < len(expression) and (expression[i] not in _CLOSING_PARENTHESES):
                    number = number + expression[i]
                    i += 1
            else:
                while i < len(expression) and (is_number(expression[i]) or expression[i] in _COMMA):
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

    for operator in _OPERATORS + _OPEN_PARENTHESES + "=":
        for sign in _SIGN:
            split = expression.split(operator + sign)
            if len(split) > 1:
                # Starting with 2nd part
                index = 1
                while index < len(split):
                    # Getting number
                    number = ""
                    i = 0
                    while i < len(split[index]):
                        if not is_number(split[index][i]) and not split[index][i] in _COMMA:
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
                    or splitted_expression[index - 1][-1] in _CLOSING_PARENTHESES
                ):
                    splitted_expression[index - 1] = splitted_expression[index - 1] + "*"
            # Checking implicit mult after the var
            if splitted_expression[index] and (
                splitted_expression[index][0].isdecimal() is True
                or splitted_expression[index][0] in _OPEN_PARENTHESES
            ):
                splitted_expression[index] = "*" + splitted_expression[index]
            index += 1
        expression = var.join(splitted_expression)
    return expression


def parse_sign(expression: str):
    """
    Removing extra _sign
    """
    while "--" in expression or "++" in expression or "-+" in expression or "+-" in expression:
        expression = (
            expression.replace("--", "+").replace("++", "+").replace("+-", "-").replace("-+", "-")
        )
    if len(expression) > 0:
        if expression[0] == "+":
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
    if var == "-":
        var = -1
    elif len(var) < 1:
        var = 1
    return float(var)


def my_round(number: float, precision: int = 6) -> float:
    """
    Round the number after 'precision' digits after the comma.
    """

    if number == float("-infinity") or number == float("infinity"):
        raise ValueError("Couln't round infinity.")

    # Checking for Nan
    if number != number:
        return number
    if precision != precision:
        raise ValueError("Precision is Nan.")

    if precision > 20 or precision < 0:
        raise ValueError("Precision should be between 0 and 20")

    return float(format(number, f".{precision}f"))


def my_abs(number: float) -> float:
    if number < 0:
        return number * -1
    return number


def my_sqrt(number: int):
    infinity_float = float("infinity")
    negative_infinity_float = float("-infinity")

    # Checking for Nan
    if number != number:
        return number

    if number == negative_infinity_float or number == infinity_float:
        return number

    if number < 0:
        raise ValueError("input should be a positive number.")

    result = float(number)
    precision = my_power(10, -15)
    index = 0
    while my_abs(number - result * result) > precision:
        last_result = result
        result = (result + number / result) / 2
        if last_result == result:
            break
        index += 1
    return my_round(result, precision=15)


def my_power(number: float, power: int) -> float:
    if power != int(power):
        raise ValueError("irrational numbers are not accepted as exponent.")

    if power == 0:
        return 1.0
    elif number == 0:
        return 0.0

    # Checking for Nan
    if power != power:
        return power
    elif number != number:
        return number

    infinity_float = float("infinity")
    negative_infinity_float = float("-infinity")
    if power == negative_infinity_float or power == infinity_float:
        return power

    result = 1.0

    if power > 0:
        while power > 0:
            result *= number
            power -= 1
            if result > 99999999999999999999999999999999:
                result = float("Infinity")
            elif result < -99999999999999999999999999999999:
                result = float("-Infinity")
            if result == float("Infinity") or result == 0 or result == float("-Infinity"):
                return result
    elif power == 0:
        result = 1
    else:
        while power < 0.0:
            result /= number
            power += 1
            if result < 0.000000000000000000000000000001:
                result = 0
            if result == float("Infinity") or result == 0 or result == float("-Infinity"):
                return result
    return result
