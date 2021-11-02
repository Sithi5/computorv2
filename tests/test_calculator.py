import pytest

from src.globals_vars import TESTS_VERBOSE
from src.expression_resolver import ExpressionResolver

from src.matrix_utils import (
    return_2d_matrix_in_str,
    identity_square_matrix_factory,
    matrix_factory,
)

from src.types.types import Matrix
from src.assignment.assigned_file import clear_assigned_file


def test_calculator_function():

    try:
        clear_assigned_file()
        resolver = ExpressionResolver(verbose=TESTS_VERBOSE)

        ret = resolver.solve(expression="f(x) = 2 *( x + 3 * (x - 4))")
        assert str(ret) == "((X-4.0)*3.0+X)*2.0"
        ret = resolver.solve(expression="f(2) = ?")
        assert str(ret) == "-8.0"
        ret = resolver.solve(expression="f(3) = ?")
        assert str(ret) == "0.0"
    except Exception:
        clear_assigned_file()
        raise
    clear_assigned_file()


def test_calculator_complex():
    resolver = ExpressionResolver(verbose=TESTS_VERBOSE)

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


def test_calculator_matrix():
    resolver = ExpressionResolver(verbose=TESTS_VERBOSE)

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

    # Matrix powered by 0, should return an identity matrix
    matrix = resolver.solve(expression="[[5,2];[1,9i]] ^ 0")
    assert return_2d_matrix_in_str(matrix=matrix) == return_2d_matrix_in_str(
        matrix=identity_square_matrix_factory(size=2)
    )
    assert return_2d_matrix_in_str(matrix=matrix) != return_2d_matrix_in_str(
        matrix=identity_square_matrix_factory(size=4)
    )

    # Matrix + Matrix not same size
    with pytest.raises(ValueError) as e:
        resolver.solve(expression="[[5,2];[1,9i]] + [[2,4]]")
    assert (
        str(e.value)
        == "For operator of type '+' between two matrix, both matrix should be of same size."
    )
    # Matrix - Matrix not same size
    with pytest.raises(ValueError) as e:
        resolver.solve(expression="[[5,2];[1,9i]] - [[2,4]]")
    assert (
        str(e.value)
        == "For operator of type '-' between two matrix, both matrix should be of same size."
    )
    # Matrix - Matrix same size
    matrix = resolver.solve(expression="[[5,2];[1,5]] - [[5,2];[1,5]]")
    assert return_2d_matrix_in_str(matrix=matrix) == return_2d_matrix_in_str(
        matrix=matrix_factory(columns_size=2, row_size=2)
    )
    assert return_2d_matrix_in_str(matrix=matrix) != return_2d_matrix_in_str(
        matrix=matrix_factory(columns_size=2, row_size=1)
    )
    # Matrix + Matrix same size
    matrix = resolver.solve(expression="[[5,5];[5,5i]] + [[5,5];[5,5i]]")
    expected_result = Matrix(value="[[10,10];[10,10i]]")
    assert return_2d_matrix_in_str(matrix=matrix) == return_2d_matrix_in_str(matrix=expected_result)

    # Matrix + Matrix same size
    matrix = resolver.solve(expression="[[(5*2)2]] + [[5]] * 2")
    expected_result = Matrix(value="[[30]]")
    assert return_2d_matrix_in_str(matrix=matrix) == return_2d_matrix_in_str(matrix=expected_result)

    # Matrix - Matrix same size
    matrix = resolver.solve(expression="[[(5)*-2];[18]] - [[5];[2]] * 2")
    expected_result = Matrix(value="[[-20][14]]")
    assert return_2d_matrix_in_str(matrix=matrix) == return_2d_matrix_in_str(matrix=expected_result)

    # Matrix * Matrix same size
    matrix = resolver.solve(expression="[[1];[2]] * [[2];[2]]/ 2")
    expected_result = Matrix(value="[[1][2]]")
    assert return_2d_matrix_in_str(matrix=matrix) == return_2d_matrix_in_str(matrix=expected_result)

    # Matrix / Matrix same size
    matrix = resolver.solve(expression="[[10];[20]] / [[2];[2]]")
    expected_result = Matrix(value="[[5][10]]")
    assert return_2d_matrix_in_str(matrix=matrix) == return_2d_matrix_in_str(matrix=expected_result)

    # Matrix % Matrix same size
    matrix = resolver.solve(expression="[[10];[3]] % [[2];[2]]")
    expected_result = Matrix(value="[[0][1]]")
    assert return_2d_matrix_in_str(matrix=matrix) == return_2d_matrix_in_str(matrix=expected_result)

    # Matrix ** Matrix column size != row size
    with pytest.raises(ValueError) as e:
        resolver.solve(expression="[[10,1];[3,1];[7,1]] ** [[2,2]]")
    assert (
        str(e.value)
        == "The number of columns in the first matrix must be equal to the number of rows in the second matrix in a matrix multiplication."
    )

    # Matrix ** Matrix column size == row size
    matrix = resolver.solve(expression="[[30,31];[32,33];[34,35]] ** [[1,2,3];[4,5,6];[7,8,9]]")
    expected_result = Matrix(value="[[196,202];[484,499];[772,796]]")
    assert return_2d_matrix_in_str(matrix=matrix) == return_2d_matrix_in_str(matrix=expected_result)

    # Matrix ** Matrix column size == row size
    matrix = resolver.solve(expression="[[30];[15]] ** [[5,2]]")
    expected_result = Matrix(value="[[180]]")
    assert return_2d_matrix_in_str(matrix=matrix) == return_2d_matrix_in_str(matrix=expected_result)

    # Matrix ** Matrix column size == row size
    matrix = resolver.solve(expression="[[30];[-15]] ** [[5,2]]")
    expected_result = Matrix(value="[[120]]")
    assert return_2d_matrix_in_str(matrix=matrix) == return_2d_matrix_in_str(matrix=expected_result)

    matrix = resolver.solve(expression="ma = [[2,2];[2,2]]")
    matrix = resolver.solve(expression="ma = ?")
    expected_result = Matrix(value="[[2,2];[2,2]]")
    assert return_2d_matrix_in_str(matrix=matrix) == return_2d_matrix_in_str(matrix=expected_result)
    matrix = resolver.solve(expression="ma * 2")
    expected_result = Matrix(value="[[4,4];[4,4]]")
    assert return_2d_matrix_in_str(matrix=matrix) == return_2d_matrix_in_str(matrix=expected_result)
    matrix = resolver.solve(expression="ma = ?")
    expected_result = Matrix(value="[[2,2];[2,2]]")
    assert return_2d_matrix_in_str(matrix=matrix) == return_2d_matrix_in_str(matrix=expected_result)


def test_calculator_quadratic_equation():
    try:
        clear_assigned_file()
        resolver = ExpressionResolver(verbose=TESTS_VERBOSE)

        ret = resolver.solve(expression="f(x) = -x ^ 2 +2x-3")
        assert str(ret) == "(0.0-X)^2.0+2.0X-3.0"
        ret = resolver.solve(expression="f(x) = 0 ?")
        assert str(ret) == "-8.0"
    except Exception:
        clear_assigned_file()
        raise
    clear_assigned_file()
