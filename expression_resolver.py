# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    expression_resolver.py                             :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: mabouce <ma.sithis@gmail.com>              +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/12/01 21:41:09 by mabouce           #+#    #+#              #
#    Updated: 2021/07/15 13:53:33 by mabouce          ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import re

from equation_solver import _EquationSolver
from calculator import _Calculator
from globals_vars import (
    _OPERATORS,
    _SIGN,
    _COMMA,
    _OPEN_PARENTHESES,
    _CLOSING_PARENTHESES,
)
from exception import NothingToDoError

from utils import (
    convert_to_tokens,
    parse_sign,
    convert_signed_number,
    add_implicit_cross_operator_for_vars,
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

    def _check_args(self):
        # Var to check operator is followed by alphanum.
        last_operator = None
        # Var to check good parentheses use.
        parentheses_count = 0
        # Checking comma is followed and preceded by a digit.
        # This is not checking the use of more than one comma in same number !
        for comma in _COMMA:
            comma_split = self.expression.split(comma)
            try:
                if len(comma_split) > 1:
                    for part in comma_split:
                        if part == comma_split[0]:
                            assert len(part) >= 1
                            assert part[-1].isdecimal()
                        elif part == comma_split[-1]:
                            assert len(part) >= 1
                            assert part[0].isdecimal()
                        else:
                            assert len(part) >= 2
                            assert part[0].isdecimal()
                            assert part[-1].isdecimal()
            except AssertionError:
                raise SyntaxError("Some numbers are not well formated (Comma error).")

        # Check allowed char.
        last_c = False
        for idx, c in enumerate(self.expression):
            if (
                c not in "="
                and c not in "?"
                and c not in _OPERATORS
                and c not in _SIGN
                and c not in _OPEN_PARENTHESES
                and c not in _CLOSING_PARENTHESES
                and not c.isalnum()
                and c not in _COMMA
            ):
                raise SyntaxError(
                    "This is not an expression or some of the operators are not reconized."
                )
            # Check multiple operators before alphanum. Check parenthesis count.
            # Checking also that a sign isn't followed by an operator
            if (
                c in _OPERATORS
                and last_operator
                and (last_operator in _OPERATORS or last_operator in _SIGN)
            ):
                raise SyntaxError(
                    "Operators must be followed by a value or a variable, not another operator."
                )
            if c in "?" and (idx != len(self.expression) - 1 or last_c is False or last_c != "="):
                if last_c is False:
                    raise SyntaxError("Operators '?' can't be in the first position.")
                else:
                    raise SyntaxError(
                        "Operators '?' must follow operator '=' and be at the end of the expression."
                    )
            elif c in "=" and (last_c is False or last_c in "="):
                if last_c is False:
                    raise SyntaxError(
                        "Equality operator '=' shouln't be placed at the first position."
                    )
                else:
                    raise SyntaxError(
                        "Equality operator '=' shouln't be follow by another equality operator."
                    )
            elif c in _OPERATORS or c in _SIGN:
                last_operator = c
            elif c.isalnum():
                last_operator = None
            elif c in _OPEN_PARENTHESES:
                parentheses_count += 1
            elif c in _CLOSING_PARENTHESES:
                parentheses_count -= 1

            if parentheses_count < 0:
                raise SyntaxError("Closing parenthesis with no opened one.")
            last_c = c
        if (
            self.expression[-1] in _OPERATORS
            or self.expression[-1] in _SIGN
            or (last_operator and last_operator in _OPERATORS)
        ):
            raise SyntaxError("Operators or sign must be followed by a value or a variable.")
        if parentheses_count != 0:
            raise SyntaxError("Problem with parenthesis.")

    def _add_implicit_cross_operator_when_parenthesis(self):
        """
        Checking for numbers before open or after closing parenthesis without sign and add a
        multiplicator operator.
        """
        # Checking open parenthesis
        for open_parenthese in _OPEN_PARENTHESES:
            splitted_expression = self.expression.split(open_parenthese)
            index = 1
            while index < len(splitted_expression):
                # Checking if previous part is not empty
                if len(splitted_expression[index - 1]) > 0:
                    # Getting previous part to check sign
                    if (
                        splitted_expression[index - 1][-1].isdecimal() is True
                        or splitted_expression[index - 1][-1] in _CLOSING_PARENTHESES
                    ):
                        splitted_expression[index - 1] = splitted_expression[index - 1] + "*"
                index += 1
            self.expression = open_parenthese.join(splitted_expression)

        # Checking closing parenthesis
        for closing_parenthese in _CLOSING_PARENTHESES:
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

    def _get_vars(self):
        vars_list = re.findall(pattern=r"[A-Z]+", string=self.expression)
        # Removing duplicate var
        self._vars_set = list(set(vars_list))

        # Prevent var in parenthesis
        index = 0
        parenthesis_counter = 0
        is_open = False
        first_open_index = 0
        for var in self._vars_set:
            while index < len(self.expression):
                if self.expression[index] in _OPEN_PARENTHESES:
                    if not is_open:
                        is_open = True
                        first_open_index = index
                    parenthesis_counter += 1
                elif self.expression[index] in _CLOSING_PARENTHESES:
                    parenthesis_counter -= 1
                if parenthesis_counter == 0 and is_open:
                    is_open = False
                    if var in self.expression[first_open_index : index + 1]:
                        raise NotImplementedError(
                            "Var cannot be inside a parenthesis for the moment."
                        )
                index += 1

    def _parse_expression(self):
        print("Expression before parsing : ", self.expression) if self._verbose is True else None

        # Removing all spaces
        self.expression = self.expression.replace(" ", "")
        # Replace ',' comma type by '.' comma.
        self.expression = self.expression.replace(",", ".")
        # Replace '{' parenthesis type by '(' parenthesis type.
        self.expression = self.expression.replace("{", "(")
        self.expression = self.expression.replace("}", ")")

        print(
            "Removing all space from the expression : ", self.expression
        ) if self._verbose is True else None

        # To put before convert_signed_number because it is creating parenthesis
        self.expression = parse_sign(self.expression)
        print("Parsing signs : ", self.expression) if self._verbose is True else None

        self._get_vars()
        print("vars = ", self._vars_set) if self._verbose is True else None

        self.expression = convert_signed_number(expression=self.expression, accept_var=True)

        print("Convert signed numbers : ", self.expression) if self._verbose is True else None

        self._add_implicit_cross_operator_when_parenthesis()
        self.expression = add_implicit_cross_operator_for_vars(self._vars_set, self.expression)

        print(
            "Convert implicit multiplication : ", self.expression
        ) if self._verbose is True else None

        # Checking args here before converting to token
        self._check_args()

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
        variable_assigment_search = re.search(pattern=r"^[a-zA-Z]+=.+", string=self.expression)
        if variable_assigment_search and self.expression[-1] == "?":
            # variable resolving.
            print("resolving variable.")
            exit()
            pass
        elif variable_assigment_search:
            print("assigning variable.")
            exit()
            pass

        # No variable/function/matrice assignation or variable/function/matrice resolving, check if it is an equation.
        equal_operator = [elem for elem in self._tokens if elem == "="]
        if len(equal_operator) == 0:
            self._solver = _Calculator()
        elif len(equal_operator) == 1:
            self._solver = _EquationSolver(_Calculator(), self._output_graph)
        else:
            raise NotImplementedError("More than one comparison is not supported for the moment.")

    def solve(self, expression: str):
        """
        Use the solver of the class set by set_solver to solve the expression.
        """
        print("\nEXPRESSION RESOLVER\n") if self._verbose is True else None
        self.expression = expression.upper()
        self._parse_expression()
        self._set_solver()
        result = self._solver.solve(
            tokens=self._tokens,
            verbose=self._verbose,
            force_calculator_verbose=self._force_calculator_verbose,
        )
        print("\nEND OF EXPRESSION RESOLVER\n----------\n") if self._verbose is True else None
        return result
