from src.types.types import Matrix


def square_matrix_factory(size: int) -> Matrix:
    if size < 1:
        raise ValueError("Matrix should be of size one minimum.")
    first_column = True
    matrice_value = "["
    for i in range(size):
        if first_column:
            first_column = False
        else:
            matrice_value += ";"
        matrice_value += "["
        first_line = True
        for j in range(size):
            if first_line:
                first_line = False
            else:
                matrice_value += ","
            matrice_value += "0.0"
        matrice_value += "]"
    matrice_value += "]"
    matrice = Matrix(value=matrice_value)
    return matrice


def identity_square_square_matrix_factory(size: int) -> Matrix:
    matrice = square_matrix_factory(size=size)
    return matrice


def print_square_matrix(matrice: Matrix) -> Matrix:
    matrice = square_matrix_factory(size=size)
    return matrice
