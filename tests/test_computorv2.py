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

from expression_resolver import ExpressionResolver


def test_computorv2_error():
    resolver = ExpressionResolver(verbose=False)

    with pytest.raises(SyntaxError) as e:
        resolver.solve(expression="x == 2")
    assert str(e.value) == "Equality operator '=' shouln't be follow by another equality operator."

    with pytest.raises(SyntaxError) as e:
        resolver.solve(expression="x = 23edd23-+-+")
    assert str(e.value) == "Operators or sign must be followed by a value or a variable."

    # resolver.solve(expression="i = 2")


def test_computorv2_parsing():
    resolver = ExpressionResolver(verbose=False)

    # Test operator '?' at the end only
    with pytest.raises(SyntaxError) as e:
        resolver.solve(expression="5 = ? 5 * 2")
    assert str(e.value) == "Operators '?' must be at the end of the expression."

    # Test operator '=' at the end only
    with pytest.raises(SyntaxError) as e:
        resolver.solve(expression="= 5 + 2")
    assert str(e.value) == "Equality operator '=' shouln't be placed at the first position."
