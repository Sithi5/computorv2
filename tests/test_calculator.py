import pytest

from src.expression_resolver import ExpressionResolver
from src.matrix_utils import square_matrix_factory


def test_calculator_complex():
    resolver = ExpressionResolver(verbose=False)

    # Simple test
    ret = resolver.solve(expression="5 * 5i")
    assert str(ret) == "25.0i"

    # Add complex
    ret = resolver.solve(expression="(123847.2193812 - 5i) + 2i")
    assert str(ret) == "123847.219381 - 3.0i"
    ret = resolver.solve(expression="(99 - 5i) - (1 +2i)")
    assert str(ret) == "98.0 - 7.0i"

    # Dividing complex
    ret = resolver.solve(expression="(5i) / 2")
    assert str(ret) == "2.5i"
    ret = resolver.solve(expression="(5i) / (5 + 255i)")
    assert str(ret) == "0.0196 + 0.000384i"

    # Mod complex
    ret = resolver.solve(expression="(5i) % 2")
    assert str(ret) == "i"
    ret = resolver.solve(expression="(123+ 5i) % 54")
    assert str(ret) == "15.0 + 5.0i"

    # Power complex
    ret = resolver.solve(expression="(5i) ^ 2")
    assert str(ret) == "-25.0"
    ret = resolver.solve(expression="(5i) ^ 0")
    assert str(ret) == "1.0"
    ret = resolver.solve(expression="(5 + 5i) ^ 2")
    assert str(ret) == "50.0i"


def test_calculator_matrice():
    resolver = ExpressionResolver(verbose=False)

    # Test undefined operation.
    with pytest.raises(ValueError) as e:
        resolver.solve(expression="[[5,2];[1,9i]] + 5")
    assert (
        str(e.value)
        == "Operator '+' have an undefined behavior between a matrix and a real/complex number."
    )
    with pytest.raises(ValueError) as e:
        resolver.solve(expression="5 - [[5,2];[1,9i]]")
    assert (
        str(e.value)
        == "Operator '-' have an undefined behavior between a matrix and a real/complex number."
    )

    # Real divided by matrix
    with pytest.raises(ValueError) as e:
        resolver.solve(expression="2 / [[5,2];[1,9i]]")
    assert (
        str(e.value)
        == "A real/complex have an undefined behavior with the following operator '/' and a matrix."
    )

    # Real modulo by matrix
    with pytest.raises(ValueError) as e:
        resolver.solve(expression="2 % [[5,2];[1,9i]]")
    assert (
        str(e.value)
        == "A real/complex have an undefined behavior with the following operator '%' and a matrix."
    )

    # Real powered by matrix
    with pytest.raises(ValueError) as e:
        resolver.solve(expression="2.15 ^ [[5,2];[1,9i]]")
    assert (
        str(e.value)
        == "A real/complex have an undefined behavior with the following operator '^' and a matrix."
    )

    # Real addition by matrix
    with pytest.raises(ValueError) as e:
        resolver.solve(expression="2 + [[5,2];[1,9i]]")
    assert (
        str(e.value)
        == "Operator '+' have an undefined behavior between a matrix and a real/complex number."
    )

    # Multiply by Natural
    ret = resolver.solve(expression="2 [[5,2];[1,9i]]")
    assert str(ret) == "[[10.0 , 4.0] ; [2.0 , 18.0i]]"

    # Dividing by Natural
    ret = resolver.solve(expression="[[5,2];[1,9i]] / 2")
    assert str(ret) == "[[2.5 , 1.0] ; [0.5 , 4.5i]]"

    # Multiply by Real
    ret = resolver.solve(expression="2.15 [[5,2];[1,9i]]")
    assert str(ret) == "[[10.75 , 4.3] ; [2.15 , 19.35i]]"

    # Dividing by Real
    ret = resolver.solve(expression="[[5,2];[1,9i]] / 2.15")
    assert str(ret) == "[[2.325581 , 0.930233] ; [0.465116 , 4.186047i]]"

    # Dividing by complex
    ret = resolver.solve(expression="[ [ 5 , 2 ] ; [ 1, 9i] ] / (5 - 2.5i)")
    assert str(ret) == "[[0.8 + 0.4i , 0.32 + 0.16i] ; [0.16 + 0.08i , -0.72 + 1.44i]]"

    # Matrix powered by negative number
    with pytest.raises(NotImplementedError) as e:
        resolver.solve(expression="[[5,2];[1,9i]] ^ -1")
    assert str(e.value) == "Powering a matrix by a negative number is not implemented yet."

    # Matrix powered by complex number
    with pytest.raises(ValueError) as e:
        resolver.solve(expression="[[5,2];[1,9i]] ^ (1 + 5i)")
    assert str(e.value) == "A matrix should be powered by Natural numbers."

    # Matrix powered by Real number
    with pytest.raises(ValueError) as e:
        resolver.solve(expression="[[5,2];[1,9i]] ^ 1.5")
    assert str(e.value) == "A matrix should be powered by Natural numbers."


def test_square_matrix_factory():
    matrix = square_matrix_factory(size=15)
