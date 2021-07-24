from computorv2.src.types.types import *

from computorv2.src.regex import (
    regex_potential_matrice,
    regex_functions,
    regex_function_name,
    regex_function_argument,
    regex_variables,
    regex_operators,
    regex_complex,
    regex_real,
)
from computorv2.globals_vars import (
    OPERATORS,
    OPERATORS_PRIORITY,
    SIGN,
    OPEN_PARENTHESES,
    CLOSING_PARENTHESES,
)


def convert_expression_to_type_list(expression: str) -> list:
    type_list: list = []

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
        # Match functions before var because can have a var inside
        elif matched_function:
            # Take first alphapart
            match_function_name = regex_function_name.match(matched_function.group(0))
            search_function_argument = regex_function_argument.search(matched_function.group(0))
            if match_function_name and search_function_argument:
                function_name = match_function_name.group(0)
                function_argument = search_function_argument.group(0)
                type_list.append(Function(name=function_name, argument=function_argument))
                match_size = len(matched_function.group(0))
            else:
                raise SyntaxError("Some numbers are not well formated : " + expression)
        # Find variables
        elif matched_variable:
            variable_name = matched_variable.group(0)
            type_list.append(Variable(name=variable_name, value=None))
            match_size = len(matched_variable.group(0))
        elif matched_operator:
            type_list.append(Operator(value=matched_operator.group(0)))
            match_size = len(matched_operator.group(0))
        # Match complex before numbers
        elif matched_complex:
            type_list.append(Complex(value=matched_complex.group(0)))
            match_size = len(matched_complex.group(0))
        elif matched_real:
            type_list.append(Real(value=matched_real.group(0)))
            match_size = len(matched_real.group(0))
        else:
            raise SyntaxError("Expression is not well formated : " + expression)

        expression = expression[match_size:]
    return type_list


def convert_variables_and_functions_to_base_type(type_listed_expression: list, assigned_list: list):
    """Convert all variables and functions from a type listed expression to their respective value.
    Raise a ValueError error if it is not resolvable."""

    def _get_variable_value(variable: Variable) -> BaseType:
        for elem in assigned_list:
            if variable.name == elem.name:
                return elem.value
        raise ValueError("Couldn't resolve the variable : ", variable.name)

    def _return_function_right_part(function: Function) -> BaseType:
        for elem in assigned_list:
            if function.name == elem.name:
                # TODO to change
                return Real("5")
        raise ValueError("Couldn't resolve the function : ", function.name)

    for index, elem in enumerate(type_listed_expression):
        if isinstance(elem, Variable):
            type_listed_expression[index] = _get_variable_value(variable=elem)
        elif isinstance(elem, Function):
            type_listed_expression[index] = _return_function_right_part(function=elem)


def sort_type_listed_expression_to_rpi(type_listed_expression: list):
    """This function will sort the type_listed expression to the RPI system."""

    res: list = []
    stack: list = []
    for elem in type_listed_expression:
        if not isinstance(elem, Operator):
            res.append(elem)
        elif elem.value in OPEN_PARENTHESES:
            stack.append(elem)
        elif elem.value in CLOSING_PARENTHESES:
            try:
                unstack = stack.pop()
                while unstack.value not in OPEN_PARENTHESES:
                    res.append(unstack)
                    unstack = stack.pop()
            except IndexError:
                raise IndexError("Bad parenthesis.")
        elif elem.value in OPERATORS + SIGN:
            try:
                unstack = stack[-1]
                while (
                    unstack.value not in OPEN_PARENTHESES
                    and OPERATORS_PRIORITY[unstack.value] >= OPERATORS_PRIORITY[elem.value]
                ):
                    res.append(stack.pop())
                    unstack = stack[-1]
            except IndexError:
                pass
            finally:
                stack.append(elem)

    return res + stack[::-1]


def print_type_listed_expression_in_str(type_listed_expression: list):
    str_expression = ""
    for elem in type_listed_expression:
        if str_expression != "":
            str_expression += " "
        str_expression += str(elem)
    print(str_expression)