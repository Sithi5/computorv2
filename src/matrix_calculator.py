from typing import Union

from src.types.types import *
from src.globals_vars import *
from src.math_utils import is_natural
from src.real_calculator import real_calculator
from src.complex_calculator import complex_calculator
from src.matrix_utils import identity_square_matrix_factory, matrix_factory


def dot_product(
    first_matrix,
    second_matrix,
    first_matrix_row_index: int,
    second_matrix_column_index: int,
    verbose: bool = False,
) -> Union[Real, Complex]:
    sum: Union[Real, Complex] = Real(0)
    index = 0
    print(
        "Doing dot product of matrix ",
        str(first_matrix),
        " and matrix ",
        str(second_matrix),
        "\n\nFirst matrix row index:\t",
        first_matrix_row_index,
        "\nSecond matrix column index:\t",
        second_matrix_column_index,
    ) if verbose is True else None
    while index < first_matrix.n:
        if (
            isinstance(
                first_matrix.value[index][first_matrix_row_index][0],
                Complex,
            )
            or isinstance(
                sum,
                Complex,
            )
            or isinstance(
                second_matrix.value[second_matrix_column_index][index][0],
                Complex,
            )
        ):
            sum = complex_calculator(
                elem_one=sum,
                elem_two=complex_calculator(
                    elem_one=first_matrix.value[index][first_matrix_row_index][0],
                    elem_two=second_matrix.value[second_matrix_column_index][index][0],
                    operator=Operator(value=MULTIPLICATION_SIGN),
                    verbose=verbose,
                ),
                operator=Operator(value=ADDITION_SIGN),
                verbose=verbose,
            )
        else:
            sum = real_calculator(
                elem_one=sum,
                elem_two=real_calculator(
                    elem_one=first_matrix.value[index][first_matrix_row_index][0],
                    elem_two=second_matrix.value[second_matrix_column_index][index][0],
                    operator=Operator(value=MULTIPLICATION_SIGN),
                    verbose=verbose,
                ),
                operator=Operator(value=ADDITION_SIGN),
                verbose=verbose,
            )
        index += 1
    return sum


def matrix_calculator(
    elem_one: Union[Real, Complex, Matrix],
    elem_two: Union[Real, Complex, Matrix],
    operator: Operator,
    verbose: bool = False,
) -> Matrix:
    """
    This method take matrix/real/complex in input and an operator and return a matrix by resolving calculation
    """
    print("\nMatrice calculator :") if verbose is True else None
    print(
        str(elem_one) + " " + str(operator) + " " + str(elem_two) + "\n"
    ) if verbose is True else None

    if not isinstance(elem_one, Matrix) and not isinstance(elem_two, Matrix):
        raise ValueError(
            """
            Wrong type in matrix calculator. Input type should be:
            At least one matrix type and Real/Complex.
            """
        )

    if (isinstance(elem_one, Matrix) and elem_one.pending_calculation) or (
        isinstance(elem_two, Matrix) and elem_two.pending_calculation
    ):
        raise ValueError(
            """
            Can't calculate matrix with prending_calculation.
            """
        )

    if (
        isinstance(elem_one, Matrix)
        and (isinstance(elem_two, Real) or isinstance(elem_two, Complex))
    ) or (
        isinstance(elem_two, Matrix)
        and (isinstance(elem_one, Real) or isinstance(elem_one, Complex))
    ):
        # CALCUL MATRIX WITH COMPLEX/REAL #

        if operator.value in SIGN:
            raise ValueError(
                "Operator '"
                + operator.value
                + "' have an undefined behavior between a matrix and a real/complex number."
            )
        if operator.value != MULTIPLICATION_SIGN and isinstance(elem_two, Matrix):
            raise ValueError(
                "A real/complex have an undefined behavior with the following operator '"
                + operator.value
                + "' and a matrix."
            )
        if isinstance(elem_one, Matrix):
            matrix: Matrix = elem_one
            complex_or_real: Union[Real, Complex] = elem_two
        else:
            matrix: Matrix = elem_two
            complex_or_real: Union[Real, Complex] = elem_one
        if operator.value == EXPONENT_SIGN:
            if not isinstance(complex_or_real, Real) or not is_natural(n=complex_or_real.value):
                raise ValueError("A matrix should be powered by Natural numbers.")
            if matrix.m != matrix.n:
                raise NotImplementedError("Powering a matrix only work for square matrix.")
            natural_exponent = float(complex_or_real.value)
            if natural_exponent > 0:
                while natural_exponent > 1:
                    matrix = matrix_calculator(
                        elem_one=matrix,
                        elem_two=matrix,
                        operator=Operator(value=MULTIPLICATION_SIGN),
                        verbose=verbose,
                    )
                    natural_exponent -= 1
            elif natural_exponent == 0:
                # Return by convention the identity matrix
                return identity_square_matrix_factory(size=matrix.m)
            else:
                raise NotImplementedError(
                    "Powering a matrix by a negative number is not implemented yet."
                )
        else:
            for column in matrix.value:
                for row in column:
                    if isinstance(row[0], Complex) or isinstance(complex_or_real, Complex):
                        row[0] = complex_calculator(
                            elem_one=row[0],
                            elem_two=complex_or_real,
                            operator=operator,
                            verbose=verbose,
                        )
                    else:
                        row[0] = real_calculator(
                            elem_one=row[0],
                            elem_two=complex_or_real,
                            operator=operator,
                            verbose=verbose,
                        )
        return matrix
        # END OF CALCUL MATRIX WITH COMPLEX/REAL #

    else:

        # CALCUL MATRIX WITH MATRIX #

        first_matrix = elem_one
        second_matrix = elem_two
        if (
            operator.value in MATRIX_OPERATORS + SIGN
            and operator.value != MATRIX_MULTIPLICATION_SIGN
        ):
            # MATRIX TERM TO TERM #

            if first_matrix.n != second_matrix.n or first_matrix.m != second_matrix.m:
                # Matrix should be of same size.
                raise ValueError(
                    "For operator of type '"
                    + operator.value
                    + "' between two matrix, both matrix should be of same size."
                )
            else:
                columns_index = 0
                matrix = matrix_factory(columns_size=first_matrix.n, row_size=first_matrix.m)
                while columns_index < first_matrix.n:
                    row_index = 0
                    while row_index < first_matrix.m:
                        if isinstance(
                            first_matrix.value[columns_index][row_index][0], Complex
                        ) or isinstance(second_matrix.value[columns_index][row_index][0], Complex):
                            matrix.value[columns_index][row_index][0] = complex_calculator(
                                elem_one=first_matrix.value[columns_index][row_index][0],
                                elem_two=second_matrix.value[columns_index][row_index][0],
                                operator=operator,
                                verbose=verbose,
                            )
                        else:
                            matrix.value[columns_index][row_index][0] = real_calculator(
                                elem_one=first_matrix.value[columns_index][row_index][0],
                                elem_two=second_matrix.value[columns_index][row_index][0],
                                operator=operator,
                            )
                        row_index += 1
                    columns_index += 1

            # END OF MATRIX TERM TO TERM  #

        elif operator.value == MATRIX_MULTIPLICATION_SIGN:

            # MATRIX MULTIPLICATION #

            if first_matrix.n != second_matrix.m:
                raise ValueError(
                    """The number of columns in the first matrix must be equal to the number of rows in the second matrix in a matrix multiplication."""
                )
            else:
                # The resulting matrix has the number of rows of the first and the number of columns of the second matrix.
                matrix = matrix_factory(columns_size=second_matrix.n, row_size=first_matrix.m)
                columns_index = 0
                while columns_index < second_matrix.n:
                    row_index = 0
                    while row_index < first_matrix.m:
                        matrix.value[columns_index][row_index][0] = dot_product(
                            first_matrix=first_matrix,
                            second_matrix=second_matrix,
                            first_matrix_row_index=row_index,
                            second_matrix_column_index=columns_index,
                            verbose=verbose,
                        )
                        row_index += 1
                    columns_index += 1

            # END OF MATRIX MULTIPLICATION #

        # END OF CALCUL MATRIX WITH MATRIX #
        else:
            raise NotImplementedError(
                "Operator '" + operator.value + "' not implemented yet for complex.",
            )
        return matrix
