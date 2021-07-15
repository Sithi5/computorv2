from os import path

from utils import (
    split_expression_parts_from_tokens,
)
from utils_saving_variables import (
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

    def solve(self, tokens: list, verbose: bool = False, force_calculator_verbose: bool = False):
        self._verbose = verbose
        self._force_calculator_verbose = force_calculator_verbose
        self._tokens = tokens
        splits_parts = split_expression_parts_from_tokens(self._tokens)
        self._left_part = splits_parts[0]
        self._right_part = splits_parts[1]

        print("\VARIABLES ASSIGNMENTS\n") if self._verbose is True else None

        self._new_var_name = "".join(self._left_part)
        if self._new_var_name.lower() == "i":
            raise SyntaxError(
                "A variable name cannot be 'i' because 'i' is kept for imaginary numbers."
            )

        variables_list = open_and_deserialize_variables_list()
        new_variable = Real(self._new_var_name, 10)
        variables_list.append(new_variable)
        print("variable_list = ", variables_list)
        serialize_and_save_variables_list(variables_list=variables_list)
        return "Assignation de variable !"