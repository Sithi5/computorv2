import pytest

from src.expression_resolver import ExpressionResolver
from src.globals_vars import TESTS_VERBOSE


def test_undefined():
    resolver = ExpressionResolver(verbose=TESTS_VERBOSE)

    with pytest.raises(ValueError) as e:
        resolver.solve(expression=" (5 + 2i)/(0.0)")
    assert (
        str(e.value) == "('The expression lead to a division zero : ', '5.0 + 2.0i', ' / ', '0.0')"
    )
    with pytest.raises(ValueError) as e:
        resolver.solve(expression=" (5 + 2i)%(0.0)")
    assert str(e.value) == "('The expression lead to a modulo zero : ', '5.0 + 2.0i', ' % ', '0.0')"
    with pytest.raises(ValueError) as e:
        resolver.solve(expression=" 5%0")
    assert str(e.value) == "('The expression lead to a modulo zero : ', '5.0', ' % ', '0.0')"
    with pytest.raises(ValueError) as e:
        resolver.solve(expression=" 5/0")
    assert str(e.value) == "('The expression lead to a division by zero : ', '5.0', ' / ', '0.0')"
