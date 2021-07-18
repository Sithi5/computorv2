from os import path

from src.types.types import *


class Assignments:
    """
    Class for assigning a var/matrice/function
    """

    def __init__(self, calculator, assigned_list):
        self._calculator = calculator
        self._assigned_list = assigned_list

    def _assign_function(self):
        new_function = self._type_listed_expression[0]
        print("_assign_function")

    def _assign_variable(self):
        new_variable = self._type_listed_expression[0]
        print("_assign_variable")

    def solve(
        self,
        type_listed_expression: list,
        verbose: bool = False,
        force_calculator_verbose: bool = False,
    ):
        """
        This method take a type_listed_expression, check if the assignment format is correct, assign a var/matrice/function and save it into a file.
        """

        self._type_listed_expression = type_listed_expression
        self._verbose = verbose
        self._force_calculator_verbose = force_calculator_verbose
        # The type_listed_expression should have at least 3 arguments and an '=' operator as a second argument.
        if (
            len(self._type_listed_expression) < 3
            or not isinstance(self._type_listed_expression[1], Operator)
            or self._type_listed_expression[1].value != "="
        ):
            raise SyntaxError(
                "Problem with assignment : the type_listed_expression is not well formated for assignment."
            )
        else:
            if isinstance(self._type_listed_expression[0], Function):
                self._assign_function()
            elif isinstance(self._type_listed_expression[0], Variable):
                self._assign_variable()
            else:
                raise SyntaxError(
                    "Problem with assignment : trying to assign to a wrong type : "
                    + self._type_listed_expression[0].type,
                )
