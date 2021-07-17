from os import path

from utils import split_expression_parts_from_tokens, convert_to_tokens
from variables_file import (
    serialize_and_save_variables_list,
    open_and_deserialize_variables_list,
)
from variables_types import *
from variables_utils import resolve_variable_value


class _VariablesAssignments:
    _tokens: list = []
    _left_part: list = []
    _right_part: list = []
    _new_var_name: str
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
        new_variable: BaseType

        print("\VARIABLES ASSIGNMENTS\n") if self._verbose is True else None

        self._new_var_name = "".join(self._left_part)
        if self._new_var_name.lower() == "i":
            raise SyntaxError(
                "A variable name cannot be named 'i' because 'i' is kept for imaginary numbers."
            )

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
        return str(
            resolve_variable_value(
                variable_to_resolve=new_variable, variables_list=self._variables_list
            )
        )
