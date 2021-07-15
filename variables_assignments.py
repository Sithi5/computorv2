from utils import (
    split_expression_parts_from_tokens,
)


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

        print("Var name is : ", self._new_var_name)

        print(self._left_part)
        print(self._right_part)
        return "Assignation de variable !"