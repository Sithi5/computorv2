from os import path
from src.calculator import Calculator
from src.assignment.assigned_file import serialize_and_save_assigned_list

from src.types.types import *
from src.type_listed_utils import convert_variables_and_functions_to_base_type


class Assignments:
    """
    Class for assigning a var/function
    """

    def __init__(self, calculator: Calculator, assigned_list: list):
        self._calculator = calculator
        self._assigned_list = assigned_list
        self._force_calculator_verbose = False

    def _assign_function(self):
        self._new_assignment = self._type_listed_expression[0]
        self._new_assignment.right_expression = self._type_listed_expression[2:]

    def _assign_variable(self):
        self._new_assignment = self._type_listed_expression[0]
        self._new_assignment.value = self._calculator.solve(
            type_listed_expression=convert_variables_and_functions_to_base_type(
                type_listed_expression=self._type_listed_expression[2:],
                assigned_list=self._assigned_list,
            ),
            verbose=self._force_calculator_verbose,
        )

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
            # Check for other assignment with same name and remove it.
            for elem in self._assigned_list:
                if elem.name == self._new_assignment.name:
                    self._assigned_list.remove(elem)
            self._assigned_list.append(self._new_assignment)
            serialize_and_save_assigned_list(assigned_list=self._assigned_list)
            return self._new_assignment.value
