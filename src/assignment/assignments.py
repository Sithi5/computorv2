from os import path

from src.utils import split_expression_parts_from_tokens
from src.assignment.assigned_file import (
    serialize_and_save_assigned_list,
)
from src.types.types import Variable


class Assignments:
    def __init__(self, calculator, assigned_list):
        self._calculator = calculator
        self._assigned_list = assigned_list

    def solve(
        self,
        type_listed_expression: list,
        verbose: bool = False,
        force_calculator_verbose: bool = False,
    ):
        self._type_listed_expression = type_listed_expression
        self._verbose = verbose
        self._force_calculator_verbose = force_calculator_verbose


class _VariablesAssignments:
    _tokens: list = []
    _left_part: list = []
    _right_part: list = []
    _new_assignment_name: str
    _new_variable_type: str = "Real"

    def __init__(self, calculator, variables_list):
        self._calculator = calculator
        self._variables_list = variables_list

    def _define_new_variable_type(self):
        self._new_variable_type = "Real"

    def solve(self, tokens: list, verbose: bool = False, force_calculator_verbose: bool = False):
        self._verbose = verbose
        self._force_calculator_verbose = force_calculator_verbose
        self._tokens = tokens
        splits_parts = split_expression_parts_from_tokens(self._tokens)
        self._left_part = splits_parts[0]
        self._right_part = splits_parts[1]

        print("\VARIABLES ASSIGNMENTS\n") if self._verbose is True else None

        self._new_assignment_name = "".join(self._left_part)
        if self._new_assignment_name.lower() == "i":
            raise SyntaxError(
                "A variable name cannot be named 'i' because 'i' is kept for imaginary numbers."
            )

        return "Nothing yet"