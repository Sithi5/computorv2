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


class Calculator:
    def __init__(self, assigned_list: list):
        self._assigned_list = assigned_list

    def _resolve_variable(self, variable: Variable) -> BaseType:

        return UnknowType(name=variable.name)

    def _resolve_function(self, function: Function, assigned_list: list) -> BaseType:
        pass

    def _replace_known_variables_or_functions_by_value(self):
        for index, elem in enumerate(self._type_listed_expression):
            if isinstance(elem, Variable):
                self._type_listed_expression[index] = self._resolve_variable(variable=elem)
            elif isinstance(elem, Function):
                self._type_listed_expression[index] = self._resolve_function(function=elem)

    def solve(self, type_listed_expression: list, verbose: bool = False) -> BaseType:
        """
        Resolving calcul from one part type_listed_expression.
        """
        self._verbose = verbose
        self._type_listed_expression = type_listed_expression
        print(
            "Resolving following type_listed_expression : ", self._type_listed_expression
        ) if self._verbose is True else None
        self._replace_known_variables_or_functions_by_value()
        print(
            "Replacing know variables and functions by their value : ", self._type_listed_expression
        ) if self._verbose is True else None
        result = Real(str(10))
        return result
