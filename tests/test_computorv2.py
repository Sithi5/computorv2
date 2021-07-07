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


def test_computorv2():
    resolver = ExpressionResolver(verbose=False)

    with pytest.raises(SyntaxError) as e:
        resolver.solve(expression="x == 2")
    assert str(e.value) == "Equality operator '=' shouln't be follow by another equality operator."

    with pytest.raises(SyntaxError) as e:
        resolver.solve(expression="x = 23edd23-+-+")
    assert str(e.value) == "Operators or sign must be followed by a value or a variable."