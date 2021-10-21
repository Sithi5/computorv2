from math import cos, sin, atan

from typing import Union

from src.globals_vars import *
from src.types.types import *
from src.types.types_utils import (
    sort_type_listed_expression_to_rpi,
    type_listed_expression_in_str,
    check_type_listed_expression_and_add_implicit_cross_operators,
    convert_variables_and_functions_to_base_type,
)
from src.math_utils import my_power, my_round, my_sqrt, is_natural, PI
from src.matrix_utils import identity_square_matrix_factory, matrix_factory


def calc_is_in_complex(elem_one: BaseType, elem_two: BaseType, operator: BaseType = None) -> bool:
    """
    This method take two type in input and return true if the result of the calcul between those two type will be in complex.
    """
    if isinstance(elem_one, Real) and isinstance(elem_two, Complex):
        return True
    elif isinstance(elem_one, Complex) and isinstance(elem_two, Real):
        return True
    elif isinstance(elem_one, Complex) and isinstance(elem_two, Complex):
        return True
    else:
        return False


def calc_is_in_real(elem_one: BaseType, elem_two: BaseType, operator: BaseType = None) -> bool:
    """
    This method take two type in input and return true if the result of the calcul between those two type will be in Real.
    """
    return isinstance(elem_one, Real) and isinstance(elem_two, Real)


def calc_is_in_matrice(elem_one: BaseType, elem_two: BaseType, operator: BaseType = None) -> bool:
    """
    This method take two type in input and return true if the result of the calcul between those two type will be a matrix type.
    """
    return isinstance(elem_one, Matrix) or isinstance(elem_two, Matrix)


class Calculator:
    def __init__(self, assigned_list: list):
        self._assigned_list = assigned_list

    def _real_calculator(self, elem_one: Real, elem_two: Real, operator: Operator) -> Real:
        """
        This method take two real type in input and an operator and return a real by resolving trivial calculation
        """

        print("\nReal calculator :") if self._verbose is True else None
        print(
            str(elem_one) + " " + str(operator) + " " + str(elem_two) + "\n"
        ) if self._verbose is True else None

        if not isinstance(elem_one, Real) or not isinstance(elem_two, Real):
            raise ValueError(
                """
                Wrong type in real calculator. Input type should be:
                Real or Complex.
                """
            )

        if operator.value == ADDITION_SIGN:
            return Real(str(my_round(float(elem_one.value) + float(elem_two.value))))
        elif operator.value == SUBSTRACTION_SIGN:
            return Real(str(my_round(float(elem_one.value) - float(elem_two.value))))
        elif operator.value == MODULO_SIGN:
            if float(elem_two.value) == 0.0:
                raise ValueError(
                    "The expression lead to a modulo zero : ",
                    str(elem_one),
                    " " + operator.value + " ",
                    str(elem_two),
                )
            return Real(str(my_round(float(elem_one.value) % float(elem_two.value))))

        elif operator.value == DIVISION_SIGN:
            if float(elem_two.value) == 0.0:
                raise ValueError(
                    "The expression lead to a division by zero : ",
                    str(elem_one),
                    " " + operator.value + " ",
                    str(elem_two),
                )
            return Real(str(my_round(float(elem_one.value) / float(elem_two.value))))
        elif operator.value == MULTIPLICATION_SIGN:
            return Real(str(my_round(float(elem_one.value) * float(elem_two.value))))
        elif operator.value == EXPONENT_SIGN:
            return Real(str(my_round(my_power(float(elem_one.value), int(float(elem_two.value))))))
        else:
            raise ValueError(
                "The expression operator is unknown : ",
                operator.value,
            )

    def _complex_calculator(
        self, elem_one: Union[Real, Complex], elem_two: Union[Real, Complex], operator: Operator
    ) -> Complex:
        """
        This method take real/complex in input and an operator and return an imaginary by resolving calculation
        """

        print("\nComplex calculator :") if self._verbose is True else None
        print(
            "(" + str(elem_one) + ")" + " " + str(operator) + " " + "(" + str(elem_two) + ")" + "\n"
        ) if self._verbose is True else None

        # Convert real into complex.
        if isinstance(elem_one, Real):
            elem_one = Complex(real_value=elem_one.value, imaginary_value=str(float(0.0)))
        if isinstance(elem_two, Real):
            elem_two = Complex(real_value=elem_two.value, imaginary_value=str(float(0.0)))

        if not isinstance(elem_one, Complex) or not isinstance(elem_two, Complex):
            raise ValueError(
                """
                Wrong type in complex calculator. Input type should be:
                Real or Complex.
                """
            )

        if operator.value == ADDITION_SIGN:
            real_value = str(my_round(float(elem_one.real.value) + float(elem_two.real.value)))
            imaginary_value = str(
                my_round(float(elem_one.imaginary.value) + float(elem_two.imaginary.value))
            )
            return Complex(
                real_value=real_value,
                imaginary_value=imaginary_value,
            )
        elif operator.value == SUBSTRACTION_SIGN:
            real_value = str(my_round(float(elem_one.real.value) - float(elem_two.real.value)))
            imaginary_value = str(
                my_round(float(elem_one.imaginary.value) - float(elem_two.imaginary.value))
            )
            return Complex(
                real_value=real_value,
                imaginary_value=imaginary_value,
            )
        elif operator.value == MULTIPLICATION_SIGN:
            # "Firsts, Outers, Inners, Lasts"
            real_value = str(
                my_round(
                    float(elem_one.real.value) * float(elem_two.real.value)
                    - float(elem_one.imaginary.value) * float(elem_two.imaginary.value)
                )
            )
            imaginary_value = str(
                my_round(
                    float(elem_one.imaginary.value) * float(elem_two.real.value)
                    + float(elem_one.real.value) * float(elem_two.imaginary.value)
                )
            )
            return Complex(
                real_value=real_value,
                imaginary_value=imaginary_value,
            )
        elif operator.value == DIVISION_SIGN:
            if float(elem_two.real.value) == 0.0 and float(elem_two.imaginary.value) == 0.0:
                raise ValueError(
                    "The expression lead to a division zero : ",
                    str(elem_one),
                    " " + operator.value + " ",
                    str(elem_two),
                )
            conjugate_value = Complex(
                real_value=elem_two.real.value,
                imaginary_value=str(float(elem_two.imaginary.value) * -1.0),
            )
            dividend: Complex = self._complex_calculator(
                elem_one=elem_one,
                elem_two=conjugate_value,
                operator=Operator(value=MULTIPLICATION_SIGN),
            )
            divider: Complex = self._complex_calculator(
                elem_one=elem_two,
                elem_two=conjugate_value,
                operator=Operator(value=MULTIPLICATION_SIGN),
            )
            if float(divider.imaginary.value) != 0.0:
                raise Exception("Unexpected error when trying to resolve a division in complex.")
            real_value = str(float(dividend.real.value) / float(divider.real.value))
            imaginary_value = str(float(dividend.imaginary.value) / float(divider.real.value))
            return Complex(
                real_value=real_value,
                imaginary_value=imaginary_value,
            )
        elif operator.value == MODULO_SIGN:
            if float(elem_two.imaginary.value) != 0.0 and float(elem_two.real.value) != 0.0:
                raise ValueError(
                    "Can only modulo by an imaginary number or by a real number. Not by a complex. Undefined behavior."
                )
            if float(elem_two.real.value) == 0.0 and float(elem_two.imaginary.value) == 0.0:
                raise ValueError(
                    "The expression lead to a modulo zero : ",
                    str(elem_one),
                    " " + operator.value + " ",
                    str(elem_two),
                )
            if float(elem_two.imaginary.value) != 0.0:
                # Modulo by an imaginary number.
                raise ValueError("Can only modulo by a real number. Not by a complex.")
            else:
                # Modulo by a real number.
                # Doing modulo of both real and imaginary separately : (a + bi) / c = a / c + bi / c
                real_value = str(float(elem_one.real.value) % float(elem_two.real.value))
                imaginary_value = str(float(elem_one.imaginary.value) % float(elem_two.real.value))
            return Complex(
                real_value=real_value,
                imaginary_value=imaginary_value,
            )
        elif operator.value == EXPONENT_SIGN:
            if float(elem_two.imaginary.value) != 0.0:
                raise NotImplementedError(
                    "Complex exponent is not implemented yet.",
                )
            if not is_natural(elem_two.real.value):
                raise NotImplementedError(
                    "Only natural exponent are accepted.",
                )

            real_value = float(elem_one.real.value)
            imaginary_value = float(elem_one.imaginary.value)
            natural_exponent = float(elem_two.real.value)

            # Particular case.
            if natural_exponent == 0.0:
                return Complex(
                    real_value=str(1.0),
                    imaginary_value=str(0.0),
                )
            elif real_value == 0.0:
                # Imaginary only.
                powered_value = my_power(number=imaginary_value, power=natural_exponent)
                # The resulted i will loop over 4 case:
                # i ^ 1 = i
                # i ^ 2 = -1
                # i ^ 3 = -i
                # i ^ 4 = 1
                if natural_exponent % 4 == 0:
                    result = Complex(
                        real_value=str(powered_value),
                        imaginary_value="0.0",
                    )
                elif natural_exponent % 4 == 1:
                    result = Complex(
                        real_value="0.0",
                        imaginary_value=str(powered_value),
                    )
                elif natural_exponent % 4 == 2:
                    result = Complex(
                        real_value=str(float(powered_value * -1.0)),
                        imaginary_value="0.0",
                    )
                elif natural_exponent % 4 == 3:
                    result = Complex(
                        real_value="0.0",
                        imaginary_value=str(float(powered_value * -1.0)),
                    )
                return result
            else:
                # Putting complex number to exponential form Z = rexp^{i a}
                # r is the module calculated following pytagore : c = sqrt(a^2 + b^2)
                r: float = my_sqrt(
                    my_power(number=real_value, power=2) + my_power(number=imaginary_value, power=2)
                )
                if real_value > 0.0:
                    a = atan(imaginary_value / real_value)
                else:
                    if imaginary_value >= 0.0:
                        a = atan(imaginary_value / real_value) + PI
                    else:
                        a = atan(imaginary_value / real_value) - PI
                e = Complex(
                    real_value=str(cos(natural_exponent * a)),
                    imaginary_value=str(sin(natural_exponent * a)),
                )
                r = Complex(
                    real_value=str(my_power(number=r, power=natural_exponent)),
                    imaginary_value="0.0",
                )
                result = self._complex_calculator(
                    elem_one=r, elem_two=e, operator=Operator(value=MULTIPLICATION_SIGN)
                )
                return result
        else:
            raise NotImplementedError(
                "Operator '" + operator.value + "' not implemented yet for complex.",
            )

    def _resolve_inside_matrice(self, matrix: Matrix) -> Matrix:
        if isinstance(matrix, Matrix) and matrix.pending_calc:

            print("\nResolve_inside_matrice :") if self._verbose is True else None
            print(str(matrix) + "\n") if self._verbose is True else None

            for column in matrix.value:
                for row in column:
                    row_save = row.copy()
                    row.clear()
                    row.append(
                        self.solve(
                            type_listed_expression=check_type_listed_expression_and_add_implicit_cross_operators(
                                type_listed_expression=row_save
                            ),
                            verbose=self._verbose,
                        )
                    )
            matrix.pending_calc = False
        return matrix

    def _matrix_calculator(
        self,
        elem_one: Union[Real, Complex, Matrix],
        elem_two: Union[Real, Complex, Matrix],
        operator: Operator,
    ) -> Matrix:
        """
        This method take matrix/real/complex in input and an operator and return a matrix by resolving calculation
        """
        print("\nMatrice calculator :") if self._verbose is True else None
        print(
            str(elem_one) + " " + str(operator) + " " + str(elem_two) + "\n"
        ) if self._verbose is True else None

        if not isinstance(elem_one, Matrix) and not isinstance(elem_two, Matrix):
            raise ValueError(
                """
                Wrong type in matrix calculator. Input type should be:
                At least one matrix type and Real/Complex.
                """
            )

        # Check for unresolved matrix and resolve it.
        self._resolve_inside_matrice(matrix=elem_one)
        self._resolve_inside_matrice(matrix=elem_two)

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
                        matrix = self._matrix_calculator(
                            elem_one=matrix,
                            elem_two=matrix,
                            operator=Operator(value=MULTIPLICATION_SIGN),
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
                            row[0] = self._complex_calculator(
                                elem_one=row[0], elem_two=complex_or_real, operator=operator
                            )
                        else:
                            row[0] = self._real_calculator(
                                elem_one=row[0], elem_two=complex_or_real, operator=operator
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
                            ) or isinstance(
                                second_matrix.value[columns_index][row_index][0], Complex
                            ):
                                matrix.value[columns_index][row_index][
                                    0
                                ] = self._complex_calculator(
                                    elem_one=first_matrix.value[columns_index][row_index][0],
                                    elem_two=second_matrix.value[columns_index][row_index][0],
                                    operator=operator,
                                )
                            else:
                                matrix.value[columns_index][row_index][0] = self._real_calculator(
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

                    def dot_product(
                        self,
                        first_matrix,
                        second_matrix,
                        first_matrix_row_index: int,
                        second_matrix_column_index: int,
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
                        ) if self._verbose is True else None
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
                                sum = self._complex_calculator(
                                    elem_one=sum,
                                    elem_two=self._complex_calculator(
                                        elem_one=first_matrix.value[index][first_matrix_row_index][
                                            0
                                        ],
                                        elem_two=second_matrix.value[second_matrix_column_index][
                                            index
                                        ][0],
                                        operator=Operator(value=MULTIPLICATION_SIGN),
                                    ),
                                    operator=Operator(value=ADDITION_SIGN),
                                )
                            else:
                                sum = self._real_calculator(
                                    elem_one=sum,
                                    elem_two=self._real_calculator(
                                        elem_one=first_matrix.value[index][first_matrix_row_index][
                                            0
                                        ],
                                        elem_two=second_matrix.value[second_matrix_column_index][
                                            index
                                        ][0],
                                        operator=Operator(value=MULTIPLICATION_SIGN),
                                    ),
                                    operator=Operator(value=ADDITION_SIGN),
                                )
                            index += 1
                        return sum

                    # The resulting matrix has the number of rows of the first and the number of columns of the second matrix.
                    matrix = matrix_factory(columns_size=second_matrix.n, row_size=first_matrix.m)
                    columns_index = 0
                    while columns_index < second_matrix.n:
                        row_index = 0
                        while row_index < first_matrix.m:
                            matrix.value[columns_index][row_index][0] = dot_product(
                                self,
                                first_matrix=first_matrix,
                                second_matrix=second_matrix,
                                first_matrix_row_index=row_index,
                                second_matrix_column_index=columns_index,
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

    def _resolve_rpi_type_listed_expression(self) -> BaseType:
        """
        This method resolve a type_listed_expression and return the result with the correct type.
        """
        stack = []
        result: BaseType

        for elem in self._type_listed_expression:
            if not isinstance(elem, Operator):
                stack.append(elem)
            else:
                if len(stack) < 2:
                    raise IndexError(
                        "There is a problem in the npi resolver, the npi_list isn't well formated."
                    )
                last_two_in_stack = stack[-2:]
                del stack[-2:]
                # Real calc
                if calc_is_in_real(elem_one=last_two_in_stack[0], elem_two=last_two_in_stack[1]):
                    result = self._real_calculator(
                        elem_one=last_two_in_stack[0], elem_two=last_two_in_stack[1], operator=elem
                    )
                # Complex calc
                elif calc_is_in_complex(
                    elem_one=last_two_in_stack[0], elem_two=last_two_in_stack[1]
                ):
                    result = self._complex_calculator(
                        elem_one=last_two_in_stack[0], elem_two=last_two_in_stack[1], operator=elem
                    )
                # Matrix calc
                elif calc_is_in_matrice(
                    elem_one=last_two_in_stack[0], elem_two=last_two_in_stack[1]
                ):

                    result = self._matrix_calculator(
                        elem_one=last_two_in_stack[0], elem_two=last_two_in_stack[1], operator=elem
                    )
                else:
                    raise Exception(
                        "Unexpected error when trying to resolve npi. Maybe your input format is not accepted?"
                    )
                stack.append(result)

        if len(stack) > 1:
            raise Exception(
                "Unexpected error when trying to resolve npi. Maybe your input format is not accepted?"
            )

        return stack[0]

    def solve(self, type_listed_expression: list, verbose: bool = False, *arg, **kwarg) -> BaseType:
        """
        Resolving calcul from one part type_listed_expression.
        """
        self._verbose = verbose
        self._type_listed_expression = convert_variables_and_functions_to_base_type(
            type_listed_expression=type_listed_expression, assigned_list=self._assigned_list
        )

        print(
            "Resolving following type_listed_expression : ", self._type_listed_expression
        ) if self._verbose is True else None

        self._type_listed_expression = sort_type_listed_expression_to_rpi(
            type_listed_expression=self._type_listed_expression
        )
        print(
            "\nExpression in RPI: ",
            type_listed_expression_in_str(type_listed_expression=self._type_listed_expression),
        ) if self._verbose is True else None

        result: BaseType = self._resolve_rpi_type_listed_expression()

        # Check for unresolved matrix and resolve it.
        result = self._resolve_inside_matrice(matrix=result)

        return result
