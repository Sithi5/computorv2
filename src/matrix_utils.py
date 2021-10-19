from src.types.types import Matrix, Real


def matrix_factory(columns_size: int, row_size: int) -> Matrix:
    """
    Create a matrix with the input sizes and all value set to 0 and return it.
    """
    if columns_size < 1 or row_size < 1:
        raise ValueError("Input size should be a strictly positive Natural number.")
    first_column = True
    matrice_value = "["
    for i in range(columns_size):
        if first_column:
            first_column = False
        else:
            matrice_value += ";"
        matrice_value += "["
        first_line = True
        for j in range(row_size):
            if first_line:
                first_line = False
            else:
                matrice_value += ","
            matrice_value += "0.0"
        matrice_value += "]"
    matrice_value += "]"
    matrix = Matrix(value=matrice_value)
    return matrix


def square_matrix_factory(size: int) -> Matrix:
    """Return a square matrix with the input size and all value set to 0."""
    return matrix_factory(columns_size=size, row_size=size)


def identity_square_matrix_factory(size: int) -> Matrix:
    matrix = square_matrix_factory(size=size)
    i = 0
    for column in matrix.value:
        j = 0
        for row in column:
            if j == i:
                row.clear()
                row.append(Real(value="1.0"))
            j += 1
        i += 1

    return matrix


def return_2d_matrix_in_str(matrix: Matrix) -> str:
    matrix_value = ""
    first_column = True

    for column in matrix.value:
        if first_column:
            first_column = False
        else:
            matrix_value += "\n"
        first_row = True
        for row in column:
            if first_row:
                first_row = False
            else:
                matrix_value += " "
            matrix_value += "["
            for elem in row:
                matrix_value += str(elem)
            matrix_value += "]"
    return "\n" + matrix_value + "\n"
