import pytest

from src.matrix_utils import (
    square_matrix_factory,
    return_2d_matrix_in_str,
    identity_square_matrix_factory,
    matrix_factory,
)
from src.types.types import Matrix


def test_matrix_factory():
    matrix = matrix_factory(columns_size=2, lines_size=1)
    assert return_2d_matrix_in_str(matrix=matrix) == return_2d_matrix_in_str(
        matrix=Matrix(value="[[0];[0]]")
    )
    matrix = matrix_factory(columns_size=1, lines_size=2)
    assert return_2d_matrix_in_str(matrix=matrix) == return_2d_matrix_in_str(
        matrix=Matrix(value="[[0,0]]")
    )
    matrix = matrix_factory(columns_size=2, lines_size=5)
    assert return_2d_matrix_in_str(matrix=matrix) == return_2d_matrix_in_str(
        matrix=Matrix(value="[[0,0,0,0,0];[0,0,0,0,0]]")
    )


def test_square_matrix_factory():
    matrix = square_matrix_factory(size=2)
    assert return_2d_matrix_in_str(matrix=matrix) == return_2d_matrix_in_str(
        matrix=Matrix(value="[[0,0];[0,0]]")
    )
    assert return_2d_matrix_in_str(matrix=matrix) != return_2d_matrix_in_str(
        matrix=Matrix(value="[[1,0];[0,0]]")
    )
    with pytest.raises(ValueError) as e:
        square_matrix_factory(size=0)
    assert str(e.value) == "Input size should be a strictly positive Natural number."


def test_identity_square_matrix_factory():
    matrix = identity_square_matrix_factory(size=2)
    assert return_2d_matrix_in_str(matrix=matrix) == return_2d_matrix_in_str(
        matrix=Matrix(value="[[1,0];[0,1]]")
    )
    assert return_2d_matrix_in_str(matrix=matrix) != return_2d_matrix_in_str(
        matrix=Matrix(value="[[0,0];[0,0]]")
    )
    assert return_2d_matrix_in_str(matrix=matrix) != return_2d_matrix_in_str(
        matrix=Matrix(value="[[0,1];[1,0]]")
    )
    assert return_2d_matrix_in_str(matrix=matrix) != return_2d_matrix_in_str(
        matrix=Matrix(value="[[1,0];[1,0]]")
    )
    matrix = identity_square_matrix_factory(size=4)
    assert return_2d_matrix_in_str(matrix=matrix) == return_2d_matrix_in_str(
        matrix=Matrix(value="[[1,0,0,0];[0,1,0,0];[0,0,1,0];[0,0,0,1]]")
    )
