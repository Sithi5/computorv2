# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    expression_resolver.py                             :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: mabouce <ma.sithis@gmail.com>              +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/12/01 21:41:09 by mabouce           #+#    #+#              #
#    Updated: 2021/10/06 17:06:29 by mabouce          ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import re
from src.types.types import BaseType, Operator

from src.assignment.assignments import Assignments
from src.calculator import Calculator
from src.globals_vars import (
    EQUALS_SIGN,
    MATRIX_MULTIPLICATION_SIGN,
    OPERATORS,
    QUESTIONS_SIGN,
    SIGN,
    COMMA,
    OPEN_PARENTHESES,
    CLOSING_PARENTHESES,
    MATRICE_CLOSING_PARENTHESES,
    MATRICE_OPEN_PARENTHESES,
)
from src.regex import regex_check_forbidden_char
from src.types.types_utils import (
    convert_expression_to_type_list,
    check_type_listed_expression_and_add_implicit_cross_operators,
)
from src.utils import (
    parse_sign,
    convert_signed_number,
    convert_expression_to_upper,
)
from src.assignment.assigned_file import (
    open_and_deserialize_assigned_list,
)


class ExpressionResolver:
    def __init__(
        self,
        verbose: bool = False,
        force_calculator_verbose: bool = False,
        output_graph: bool = False,
    ):
        self.verbose = verbose
        self._output_graph = output_graph
        self.force_calculator_verbose = force_calculator_verbose
        self._assigned_list = open_and_deserialize_assigned_list()

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
        # Var to check good matrix parentheses use.
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
                raise SyntaxError("Closing matrix parenthesis with no opened one.")
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
            raise SyntaxError("Problem with matrix parenthesis.")

    def _parse_expression(self):
        print("Expression before parsing : ", self.expression) if self.verbose is True else None

        # Removing all spaces
        self.expression = self.expression.replace(" ", "")
        # Replace '{' parenthesis type by '(' parenthesis type.
        self.expression = self.expression.replace("{", OPEN_PARENTHESES)
        self.expression = self.expression.replace("}", CLOSING_PARENTHESES)
        self.expression = convert_expression_to_upper(input_string=self.expression)

        print(
            "Removing all space from the expression : ", self.expression
        ) if self.verbose is True else None

        # Converting operator '**' for matricial multiplication to '@'
        self.expression = self.expression.replace("**", MATRIX_MULTIPLICATION_SIGN)
        print("Converting operators : ", self.expression) if self.verbose is True else None

        # To put before convert_signed_number because it is creating parenthesis
        self.expression = parse_sign(self.expression)
        print("Parsing signs : ", self.expression) if self.verbose is True else None

        self.expression = convert_signed_number(expression=self.expression, accept_var=True)

        print("Convert signed numbers : ", self.expression) if self.verbose is True else None

        # Checking args here before converting to type list
        self._check_args()

        # Convert to type list
        self.type_listed_expression = convert_expression_to_type_list(expression=self.expression)

        print(
            "convert_expression_to_type_list : ", self.type_listed_expression
        ) if self.verbose is True else None

        self.type_listed_expression = check_type_listed_expression_and_add_implicit_cross_operators(
            type_listed_expression=self.type_listed_expression
        )

        print(
            "check_type_listed_expression_and_add_implicit_cross_operators : ",
            self.type_listed_expression,
        ) if self.verbose is True else None

    def _set_solver(self):
        """
        Setting the right class to solve the expression
        """
        calculator = Calculator(assigned_list=self._assigned_list)
        if (
            EQUALS_SIGN not in self.expression
            or isinstance(self.type_listed_expression[-1], Operator)
            and self.type_listed_expression[-1].value == QUESTIONS_SIGN
        ):
            print("\nRESOLVING INSTANCE\n") if self.verbose is True else None
            self._solver = calculator
        else:
            print("\nVARIABLE ASSIGNMENT\n") if self.verbose is True else None
            self._solver = Assignments(
                calculator=calculator,
                assigned_list=self._assigned_list,
            )

    def solve(self, expression: str):
        """
        Use the solver of the class set by set_solver to solve the expression.
        """
        print("\nEXPRESSION RESOLVER\n") if self.verbose is True else None
        if expression == "":
            return "Nothing to solve."
        else:
            self.expression = expression
            self._parse_expression()
            self._set_solver()
            result: BaseType = self._solver.solve(
                type_listed_expression=self.type_listed_expression,
                verbose=self.verbose,
                force_calculator_verbose=self.force_calculator_verbose,
            )
            print("\nEND OF EXPRESSION RESOLVER\n----------\n") if self.verbose is True else None
            return result
