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
    resolver.solve(expression="x == 2")
