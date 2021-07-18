# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    expression_resolver.py                             :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: mabouce <ma.sithis@gmail.com>              +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/12/01 21:41:09 by mabouce           #+#    #+#              #
#    Updated: 2021/07/18 12:30:30 by mabouce          ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import re

from src.equation_solver import _EquationSolver
from src.calculator import _Calculator
from src.variables.variables_assignments import _VariablesAssignments
from globals_vars import (
    OPERATORS,
    SIGN,
    COMMA,
    OPEN_PARENTHESES,
    CLOSING_PARENTHESES,
    MATRICE_CLOSING_PARENTHESES,
    MATRICE_OPEN_PARENTHESES,
)
from src.regex import regex_check_forbidden_char
from src.types.types_utils import convert_expression_to_type_list
from src.utils import (
    convert_to_tokens,
    parse_sign,
    convert_signed_number,
    convert_expression_to_upper,
)
from src.variables.variables_file import (
    open_and_deserialize_variables_list,
)


class ExpressionResolver:
    def __init__(
        self,
        verbose: bool = False,
        force_calculator_verbose: bool = False,
        output_graph: bool = False,
    ):
        self._verbose = verbose
        self._output_graph = output_graph
        self._force_calculator_verbose = force_calculator_verbose
        self._variables_list = open_and_deserialize_variables_list()

    def _check_args(self):
        for comma in COMMA:
            # Check if there is more than one comma in numbers
            check_error_multiple_comma_in_one_number = re.search(
                pattern=rf"\d+[{comma}]\d+[{comma}]", string=self.expression
            )
            # Check if comma are followed or preceded by a digit
            check_error_comma_is_not_followed_by_digit = re.search(
                pattern=rf"\d+[{comma}](?!\d)", string=self.expression
            )
            check_error_comma_is_not_preceded_by_digit = re.search(
                pattern=rf"^[{comma}]|[^\d][{comma}]\d+", string=self.expression
            )
            if (
                check_error_multiple_comma_in_one_number
                or check_error_comma_is_not_followed_by_digit is not None
                or check_error_comma_is_not_preceded_by_digit is not None
            ):
                raise SyntaxError("Some numbers are not well formated (Comma error).")

        # Check allowed char
        match_forbidden_char = regex_check_forbidden_char.search(string=self.expression)
        if match_forbidden_char:
            raise SyntaxError(
                "This is not an expression or some of the characters are not reconized : '"
                + match_forbidden_char[0]
                + "'"
            )

        # Var to check operator is followed by alphanum.
        last_operator = None
        # Var to check good parentheses use.
        parentheses_count = 0
        # Var to check good matrice parentheses use.
        matrice_parentheses_count = 0
        last_char = False
        for idx, c in enumerate(self.expression):
            # Check multiple operators before alphanum. Check parenthesis count.
            # Checking also that a sign isn't followed by an operator
            if (
                c in OPERATORS
                and last_operator
                and (last_operator in OPERATORS or last_operator in SIGN)
            ):
                raise SyntaxError(
                    "Operators must be followed by a value or a variable, not another operator."
                )
            if c in "?" and (
                idx != len(self.expression) - 1 or last_char is False or last_char != "="
            ):
                if last_char is False:
                    raise SyntaxError("Operators '?' can't be in the first position.")
                else:
                    raise SyntaxError(
                        "Operators '?' must follow operator '=' and be at the end of the expression."
                    )
            elif c in "=" and (last_char is False or last_char in "="):
                if last_char is False:
                    raise SyntaxError(
                        "Equality operator '=' shouln't be placed at the first position."
                    )
                else:
                    raise SyntaxError(
                        "Equality operator '=' shouln't be follow by another equality operator."
                    )
            elif c in OPERATORS or c in SIGN:
                last_operator = c
            elif c.isalnum():
                last_operator = None
            elif c in OPEN_PARENTHESES:
                parentheses_count += 1
            elif c in MATRICE_OPEN_PARENTHESES:
                matrice_parentheses_count += 1
            elif c in CLOSING_PARENTHESES:
                parentheses_count -= 1
            elif c in MATRICE_CLOSING_PARENTHESES:
                matrice_parentheses_count -= 1

            if parentheses_count < 0:
                raise SyntaxError("Closing parenthesis with no opened one.")
            if matrice_parentheses_count < 0:
                raise SyntaxError("Closing matrice parenthesis with no opened one.")
            last_char = c
        if (
            self.expression[-1] in OPERATORS
            or self.expression[-1] in SIGN
            or (last_operator and last_operator in OPERATORS)
        ):
            raise SyntaxError("Operators or sign must be followed by a value or a variable.")
        if parentheses_count != 0:
            raise SyntaxError("Problem with parenthesis.")
        if matrice_parentheses_count != 0:
            raise SyntaxError("Problem with matrice parenthesis.")

    def _add_implicit_cross_operator_when_parenthesis(self):
        """
        Checking for numbers before open or after closing parenthesis without sign and add a
        multiplicator operator.
        """
        # Checking open parenthesis
        for open_parenthese in OPEN_PARENTHESES:
            splitted_expression = self.expression.split(open_parenthese)
            index = 1
            while index < len(splitted_expression):
                # Checking if previous part is not empty
                if len(splitted_expression[index - 1]) > 0:
                    # Getting previous part to check sign
                    if (
                        splitted_expression[index - 1][-1].isdecimal() is True
                        or splitted_expression[index - 1][-1] in CLOSING_PARENTHESES
                    ):
                        splitted_expression[index - 1] = splitted_expression[index - 1] + "*"
                index += 1
            self.expression = open_parenthese.join(splitted_expression)

        # Checking closing parenthesis
        for closing_parenthese in CLOSING_PARENTHESES:
            splitted_expression = self.expression.split(closing_parenthese)
            index = 0
            while index < len(splitted_expression) - 1:
                # Getting previous part to check sign
                if (
                    splitted_expression[index + 1]
                    and splitted_expression[index + 1][0].isdecimal() is True
                ):
                    splitted_expression[index + 1] = "*" + splitted_expression[index + 1]
                index += 1
            self.expression = closing_parenthese.join(splitted_expression)

    def _removing_trailing_zero_and_converting_numbers_to_float(self):
        for index, token in enumerate(self._tokens):
            if token.isdecimal():
                self._tokens[index] = str(float(token))
                if "e" in self._tokens[index]:
                    self._tokens[index] = f"{float(token):.6f}"
                elif "inf" in self._tokens[index]:
                    raise ValueError(
                        "A number is too big, no input number should reach float inf or -inf."
                    )

    def _parse_expression(self):
        print("Expression before parsing : ", self.expression) if self._verbose is True else None

        # Removing all spaces
        self.expression = self.expression.replace(" ", "")
        # Replace '{' parenthesis type by '(' parenthesis type.
        self.expression = self.expression.replace("{", "(")
        self.expression = self.expression.replace("}", ")")
        self.expression = convert_expression_to_upper(input_string=self.expression)

        print(
            "Removing all space from the expression : ", self.expression
        ) if self._verbose is True else None

        # To put before convert_signed_number because it is creating parenthesis
        self.expression = parse_sign(self.expression)
        print("Parsing signs : ", self.expression) if self._verbose is True else None

        self.expression = convert_signed_number(expression=self.expression, accept_var=True)

        print("Convert signed numbers : ", self.expression) if self._verbose is True else None

        # Checking args here before converting to token
        self._check_args()

        # Convert to type_list
        self.type_listed_expression = convert_expression_to_type_list(expression=self.expression)

        exit()
        # Transforming expression to tokens
        self._tokens = convert_to_tokens(self.expression)

        print("Convert to token : ", self._tokens) if self._verbose is True else None
        self._removing_trailing_zero_and_converting_numbers_to_float()
        print(
            "Removing extra zero and converting numbers to float: ", self._tokens
        ) if self._verbose is True else None

    def _set_solver(self):
        """
        Setting the right class to solve the expression
        """
        # Computorv2 part, variable/function/matrice assignation or variable/function/matrice resolving.
        if re.search(pattern=r"^[a-zA-Z]+=.+", string=self.expression):
            print("assigning variable.")
            self._solver = _VariablesAssignments(
                calculator=_Calculator(), variables_list=self._variables_list
            )
        elif re.search(pattern=r".*[a-zA-Z]+.*=.*[?]", string=self.expression):
            # variable resolving.
            print("resolving expression with stored variable.")
            pass
        else:
            self.expression = self.expression[:-2]
            # No variable/function/matrice assignation or variable/function/matrice resolving, check if it is an equation.
            equal_operator = [elem for elem in self._tokens if elem == "="]
            if len(equal_operator) == 0:
                self._solver = _Calculator()
            elif len(equal_operator) == 1:
                self._solver = _EquationSolver(
                    calculator=_Calculator(), output_graph=self._output_graph
                )
            else:
                raise NotImplementedError(
                    "More than one comparison is not supported for the moment."
                )

    def solve(self, expression: str):
        """
        Use the solver of the class set by set_solver to solve the expression.
        """
        print("\nEXPRESSION RESOLVER\n") if self._verbose is True else None
        self.expression = expression
        self._parse_expression()
        self._set_solver()
        result = self._solver.solve(
            tokens=self._tokens,
            verbose=self._verbose,
            force_calculator_verbose=self._force_calculator_verbose,
        )
        print("\nEND OF EXPRESSION RESOLVER\n----------\n") if self._verbose is True else None
        return result
