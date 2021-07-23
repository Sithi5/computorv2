from src.types.types import *


def convert_variables_and_functions_to_base_type(type_listed_expression: list, assigned_list: list):
    """Convert all variables and functions from a type listed expression to their respective value.
    Raise a ValueError error if it is not resolvable."""

    def _resolve_variable(variable: Variable) -> BaseType:
        for elem in assigned_list:
            if variable.name == elem.name:
                return elem.value
        raise ValueError("Couldn't resolve the variable : ", variable.name)

    def _resolve_function(function: Function) -> BaseType:
        for elem in assigned_list:
            if function.name == elem.name:
                # TODO to change
                return Real("5")
        raise ValueError("Couldn't resolve the function : ", function.name)

    for index, elem in enumerate(type_listed_expression):
        if isinstance(elem, Variable):
            type_listed_expression[index] = _resolve_variable(variable=elem)
        elif isinstance(elem, Function):
            type_listed_expression[index] = _resolve_function(function=elem)
