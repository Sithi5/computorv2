# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    calculator.py                                      :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: mabouce <ma.sithis@gmail.com>              +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/12/01 20:27:15 by mabouce           #+#    #+#              #
#    Updated: 2021/07/18 18:24:24 by mabouce          ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from src.types.types import *
from src.types.types_utils import (
    sort_type_listed_expression_to_rpi,
    type_listed_expression_in_str,
)
from src.math_functions import is_real, my_power, my_round


class Calculator:
    def __init__(self, assigned_list: list):
        self._assigned_list = assigned_list

    def _real_calculator(self, real_one: Real, real_two: Real, operator: Operator) -> Real:
        if operator.value == "+":
            return Real(str(my_round(float(real_one.value) + float(real_two.value))))
        elif operator.value == "-":
            return Real(str(my_round(float(real_one.value) - float(real_two.value))))
        elif operator.value == "%":
            if float(real_two.value) == 0.0:
                raise ValueError(
                    "The expression lead to a modulo zero : ",
                    float(real_one.value),
                    " " + operator.value + " ",
                    float(real_two.value),
                )
            return Real(str(my_round(float(real_one.value) % float(real_two.value))))

        elif operator.value == "/":
            if float(real_two.value) == 0.0:
                raise ValueError(
                    "The expression lead to a division by zero : ",
                    float(real_one.value),
                    " " + operator.value + " ",
                    float(real_two.value),
                )
            return Real(str(my_round(float(real_one.value) / float(real_two.value))))
        elif operator.value == "*":
            return Real(str(my_round(float(real_one.value) * float(real_two.value))))
        elif operator.value == "^":
            return Real(str(my_round(my_power(float(real_one.value), int(float(real_two.value))))))
        else:
            raise ValueError(
                "The expression operator is unknown : ",
                operator.value,
            )

    def _resolve_rpi_type_listed_expression(self) -> BaseType:
        stack = []
        result: BaseType

        for elem in self._type_listed_expression:
            if not isinstance(elem, Operator):
                stack.append(elem)
            else:
                if len(stack) < 2:
                    raise IndexError(
                        "There is a problem in the npi resolver, the npi_list isn't well formated."
                    )
                last_two_in_stack = stack[-2:]
                del stack[-2:]
                # Real calc
                if isinstance(last_two_in_stack[0], Real) and isinstance(
                    last_two_in_stack[1], Real
                ):
                    result = self._real_calculator(
                        real_one=last_two_in_stack[0], real_two=last_two_in_stack[1], operator=elem
                    )
                else:
                    result = Real(str(10))
                stack.append(result)

        if len(stack) > 1:
            raise Exception(
                "Unexpected error when trying to resolve npi. Maybe your input format is not accepted?"
            )

        return stack[0]

    def solve(self, type_listed_expression: list, verbose: bool = False, *arg, **kwarg) -> BaseType:
        """
        Resolving calcul from one part type_listed_expression.
        """
        self._verbose = verbose
        self._type_listed_expression = type_listed_expression
        print(
            "Resolving following type_listed_expression : ", self._type_listed_expression
        ) if self._verbose is True else None
        self._type_listed_expression = sort_type_listed_expression_to_rpi(
            type_listed_expression=self._type_listed_expression
        )
        if self._verbose is True:
            print(
                "\nExpression in RPI: ",
                type_listed_expression_in_str(type_listed_expression=self._type_listed_expression),
            )
        result = self._resolve_rpi_type_listed_expression()
        return result
