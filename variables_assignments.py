import re
from os import path

from utils import split_expression_parts_from_tokens, convert_to_tokens
from variables_file import (
    serialize_and_save_variables_list,
    open_and_deserialize_variables_list,
)
from variables_types import *


class _VariablesAssignments:
    _tokens: list = []
    _left_part: list = []
    _right_part: list = []
    _new_var_name: str

    def __init__(self, calculator):
        self._calculator = calculator

    def _replace_variables_by_values(self):
        """
        Check for additional variables in the right part of assignment and replace it by there respective value.
        """
        for variable in self._variables_list:
            for index, token in enumerate(self._right_part):
                if variable.name == str(token):
                    variable_tokens = convert_to_tokens(variable.value))
                    self._right_part = (
                        self._right_part[: index - 1]
                        + variable_tokens
                        + self._right_part[index + 1 :]
                    )
                if str(token) == "I":
                    token = "i"

    def resolve_assignation(self):
        pass

    def solve(self, tokens: list, verbose: bool = False, force_calculator_verbose: bool = False):
        self._verbose = verbose
        self._new_variable_type: str = "Real"
        self._force_calculator_verbose = force_calculator_verbose
        self._tokens = tokens
        splits_parts = split_expression_parts_from_tokens(self._tokens)
        self._left_part = splits_parts[0]
        self._right_part = splits_parts[1]
        new_variable: BaseType

        print("\VARIABLES ASSIGNMENTS\n") if self._verbose is True else None

        self._new_var_name = "".join(self._left_part)
        if self._new_var_name.lower() == "i":
            raise SyntaxError(
                "A variable name cannot be named 'i' because 'i' is kept for imaginary numbers."
            )

        self._variables_list = open_and_deserialize_variables_list()

        self._replace_variables_by_values()
        if self._resolvable_assignation is True:
            self.resolve_assignation()
        if self._new_variable_type == "Real":
            new_variable = Real(self._new_var_name, self._right_part)
        elif self._new_variable_type == "Matrice":
            new_variable = Matrice(self._new_var_name, self._right_part)
        elif self._new_variable_type == "Complex":
            new_variable = Complex(self._new_var_name, self._right_part)
        else:
            new_variable = Function(self._new_var_name, self._right_part)

        # Check if the variable already exist, if it exist, delete old one.
        for variable in self._variables_list:
            if variable.name == str(self._new_var_name):
                self._variables_list.remove(variable)
        self._variables_list.append(new_variable)
        serialize_and_save_variables_list(variables_list=self._variables_list)
        return str(new_variable.value)