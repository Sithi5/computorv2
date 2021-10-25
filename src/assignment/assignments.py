from typing import Union

from src.calculator import Calculator
from src.assignment.assigned_file import serialize_and_save_assigned_list

from src.types.types import *


class Assignments:
    """
    Class for assigning a var/function
    """

    def __init__(self, calculator: Calculator, assigned_list: list):
        self._calculator = calculator
        self._assigned_list = assigned_list

    def _assign_function(self):
        print("ASSIGNING FUNCTION") if self._verbose is True else None
        if not isinstance(self._new_assignment.argument, Variable):
            raise SyntaxError("The argument of the function should be a variable for assignment.")
        self._new_assignment.value = self._type_listed_expression[2:]

    def _assign_variable(self):
        print("ASSIGNING VARIABLE") if self._verbose is True else None
        self._new_assignment.value = self._calculator.solve(
            type_listed_expression=self._type_listed_expression[2:],
            verbose=self._force_calculator_verbose,
        )

    def solve(
        self,
        type_listed_expression: list,
        verbose: bool = False,
        force_calculator_verbose: bool = False,
    ) -> Union[BaseType, Unresolved]:
        """
        This method take a type_listed_expression, check if the assignment format is correct, assign a var/matrix/function and save it into a file.
        """

        self._type_listed_expression = type_listed_expression
        self._verbose = verbose
        self._force_calculator_verbose = force_calculator_verbose

        print(
            "\nAssigning following type_listed_expression : ", self._type_listed_expression
        ) if self._verbose is True else None

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
                self._new_assignment = self._type_listed_expression[0]
                self._assign_function()
            elif isinstance(self._type_listed_expression[0], Variable):
                self._new_assignment = self._type_listed_expression[0]
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

            try:
                # Try to see if the functions/var is already resolvable or if we can get a reduce form.
                return self._calculator.solve(
                    type_listed_expression=self._new_assignment.value,
                    reduce_form_allowed=True,
                    verbose=self._force_calculator_verbose,
                )
            except Exception:
                return self._new_assignment
