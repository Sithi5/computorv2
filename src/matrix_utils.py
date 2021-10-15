from src.types.types import Matrix, Real


def square_matrix_factory(size: int) -> Matrix:
    if size < 1:
        raise ValueError("Input size should be a strictly positive Natural number.")
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
    matrix = Matrix(value=matrice_value)
    return matrix


def identity_square_matrix_factory(size: int) -> Matrix:
    matrix = square_matrix_factory(size=size)
    i = 0
    for column in matrix.value:
        j = 0
        for line in column:
            if j == i:
                line.clear()
                line.append(Real(value="1.0"))
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
        first_line = True
        for line in column:
            if first_line:
                first_line = False
            else:
                matrix_value += " "
            matrix_value += "["
            matrix_value += str(line[0])
            matrix_value += "]"
    return "\n" + matrix_value + "\n"
