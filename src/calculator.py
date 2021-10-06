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

import logging

from src.types.types import *
from src.types.types_utils import (
    sort_type_listed_expression_to_rpi,
    type_listed_expression_in_str,
)


class Calculator:
    def __init__(self, assigned_list: list):
        self._assigned_list = assigned_list

    def _resolve_rpi_type_listed_expression(self) -> BaseType:
        return Real(str(10))

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
