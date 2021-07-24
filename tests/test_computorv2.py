# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    test_computorv2.py                                 :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: mabouce <ma.sithis@gmail.com>              +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2021/07/07 16:38:01 by mabouce           #+#    #+#              #
#    Updated: 2021/07/07 16:38:01 by mabouce          ###   ########.fr        #
#                                                                              #
# **************************************************************************** #
import pytest

from src.types.types import Variable
from src.calculator import Calculator
from src.types import *
from src.expression_resolver import ExpressionResolver

resolver = ExpressionResolver(verbose=False)


def test_computorv2_error():

    with pytest.raises(SyntaxError) as e:
        resolver.solve(expression="x == 2")
    assert str(e.value) == "Equality operator '=' shouln't be follow by another equality operator."

    with pytest.raises(SyntaxError) as e:
        resolver.solve(expression="x = 23edd23-+-+")
    assert str(e.value) == "Operators or sign must be followed by a value or a variable."

    # resolver.solve(expression="i = 2")


def test_computorv2_parsing():

    # # Test operator '?' at the end only
    # with pytest.raises(SyntaxError) as e:
    #     resolver.solve(expression="5 = ? 5 * 2")
    # assert str(e.value) == "Operators '?' must be at the end of the expression."

    # # Test operator '=' at the end only
    # with pytest.raises(SyntaxError) as e:
    #     resolver.solve(expression="= 5 + 2")
    # assert str(e.value) == "Equality operator '=' shouln't be placed at the first position."

    # Test wrong char
    with pytest.raises(SyntaxError) as e:
        resolver.solve(expression="mab+{5&'}")
    assert (
        str(e.value)
        == "This is not an expression or some of the characters are not reconized : '&'"
    )

    # Test variable name i
    with pytest.raises(SyntaxError) as e:
        resolver.solve(expression="i=500")
    assert (
        str(e.value)
        == "A variable name cannot be named 'i' because 'i' is kept for imaginary numbers."
    )

    with pytest.raises(SyntaxError) as e:
        resolver.solve(expression="I=500")
    assert (
        str(e.value)
        == "A variable name cannot be named 'i' because 'i' is kept for imaginary numbers."
    )


def test_computorv2_assignment():

    # Test sign before var
    resolver.solve(expression="+X = 10")

    # Test sign before var
    resolver.solve(expression="-X = 10")

    # Test more complicated assignment
    resolver.solve(expression="X = X")


def test_resolve_variable():
    assigned_list = list(Variable(name="X"))
    calculator = Calculator(assigned_list=assigned_list)
    ret = calculator._resolve_variable(Variable(name="X"))