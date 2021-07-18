from src.types.types import *

from src.regex import (
    regex_potential_matrice,
    regex_functions,
    regex_function_name,
    regex_function_argument,
    regex_variables,
    regex_operators,
    regex_complex,
    regex_real,
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
            raise SyntaxError("Expression is not well formated : " + expression)

        expression = expression[match_size:]
    print("type_list = ", type_list)
    return type_list