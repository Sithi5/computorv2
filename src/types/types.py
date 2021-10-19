from src.globals_vars import (
    OPERATORS,
    SIGN,
    OPEN_PARENTHESES,
    CLOSING_PARENTHESES,
    MATRICE_OPEN_PARENTHESES,
    MATRICE_LINE_SEPARATOR,
    MATRICE_COLUMN_SEPARATOR,
    MATRICE_CLOSING_PARENTHESES,
)

from src.regex import regex_matrice_column, regex_complex, regex_real, regex_operators_parenthesis
from src.math_utils import is_real, my_round, my_abs

# from src.types.types_utils import (
#     convert_expression_to_type_list,
#     check_type_listed_expression_and_add_implicit_cross_operators,
# )


class BaseType:
    """Default class for Type. Should be used as an abstract class."""

    type: str

    @property
    def value(self):
        return self._value

    def __init__(self):
        self.type = self.__class__.__name__

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return self.__class__.__name__ + "('" + str(self) + "')"


class Real(BaseType):
    """Real type, the input value should be a real number."""

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value: str):
        if is_real(value):
            self._value = value
        else:
            raise SyntaxError(
                "An error occured when trying to create "
                + self.__class__.__name__
                + " object with the value : "
                + value
            )

    def __init__(self, value: str):
        super().__init__()
        self.value = value

    def __str__(self) -> str:
        return str(my_round(float(self.value)))


class Imaginary(BaseType):
    """Real type, the input value should be a real number."""

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value: str):
        try:
            if value != "":
                if value[-1] == "i":
                    value = value.replace("i", "")
                    if value == "":
                        value = "1.0"
                if is_real(value):
                    self._value = value
                else:
                    raise SyntaxError()
            else:
                raise SyntaxError()
        except SyntaxError:
            raise SyntaxError(
                "An error occured when trying to create "
                + self.__class__.__name__
                + " object with the value : "
                + value
            )

    def __init__(self, value: str):
        super().__init__()
        self.value = value

    def __str__(self) -> str:
        return str(my_round(float(self.value)))


class Complex(BaseType):
    """
    Complex type, take two input values:
    Example:
    -   Real + 15i
    """

    @property
    def real(self):
        return self._real

    @real.setter
    def real(self, real: Real):
        self._real = real

    @property
    def imaginary(self):
        return self._imaginary

    @imaginary.setter
    def imaginary(self, imaginary: Imaginary):
        self._imaginary = imaginary

    def __init__(self, real_value: str, imaginary_value: str):
        super().__init__()
        try:
            self.real = Real(value=real_value)
            self.imaginary = Imaginary(value=imaginary_value)
        except SyntaxError as e:
            raise SyntaxError(
                "An error occured when trying to create "
                + self.__class__.__name__
                + " object: "
                + e.msg
            )

    def __str__(self) -> str:
        if float(self.imaginary.value) == 0.0 and float(self.real.value) == 0.0:
            return str(0.0)
        elif float(self.real.value) == 0.0:
            if float(self.imaginary.value) == 1.0:
                return "i"
            else:
                return str(self.imaginary) + "i"
        elif float(self.imaginary.value) == 0.0:
            return str(self.real)
        else:
            if float(self.imaginary.value) > 0.0:
                return str(self.real) + " + " + str(self.imaginary) + "i"
            else:
                return str(self.real) + " - " + str(my_abs(float(self.imaginary.value))) + "i"


class Matrix(BaseType):
    """
    Matrix type, take a matrix like in input values:
    Example:
    -   [[5,3]]
    -   [[5,3];[3i + 2.5 ,8]]
    The matrix could have pending calcul inside, in that case the 'pending_calc' should be set to true at the initialization.
    """

    n: int  # Number of columns of the matrix
    m: int  # Number of lines of the matrix

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value: str):
        try:
            self._value = value
            matrice_column: list = []
            # [*.]
            if value[0] != MATRICE_OPEN_PARENTHESES or value[-1] != MATRICE_CLOSING_PARENTHESES:
                raise SyntaxError()
            # Remove first matrix parentheses
            value = value[1:-1]
            if len(value) > 0:

                # While there is a column:
                matrix_column_expected = False
                while value:
                    matched_matrice_column = regex_matrice_column.match(string=value)
                    if matched_matrice_column:
                        matrix_column_expected = False
                        value = value[len(matched_matrice_column.group(0)) :]
                        if self.n == -1:
                            # initialize total column.
                            self.n = 1

                        matrice_line: list = []

                        # Remove matrice_column parentheses
                        matched_matrice_column = matched_matrice_column.group(0)[1:-1]

                        matched_lines = matched_matrice_column.split(MATRICE_LINE_SEPARATOR)
                        for line in matched_lines:
                            if line == "":
                                # Empty line
                                raise SyntaxError()
                        if self.m == -1:
                            # Set the total line.
                            self.m = len(matched_lines)
                        elif self.m != len(matched_lines):
                            # Error line are not the same size.
                            raise SyntaxError()

                        for line in matched_lines:

                            type_list: list = []

                            while line:
                                # Convert inside line expression to type_listed (same way than convert_expression_to_type_list function).
                                matched_complex = regex_complex.match(string=line)
                                matched_real = regex_real.match(string=line)
                                matched_operator = regex_operators_parenthesis.match(string=line)
                                if matched_operator:
                                    type_list.append(Operator(value=matched_operator.group(0)))
                                    match_size = len(matched_operator.group(0))
                                elif matched_complex:
                                    imaginary_value = matched_complex.group(0)
                                    type_list.append(
                                        Complex(
                                            real_value=str(float(0.0)),
                                            imaginary_value=imaginary_value,
                                        )
                                    )
                                    match_size = len(matched_complex.group(0))
                                elif matched_real:
                                    type_list.append(Real(value=matched_real.group(0)))
                                    match_size = len(matched_real.group(0))
                                else:
                                    raise SyntaxError()
                                line = line[match_size:]

                            matrice_line.append(type_list.copy())

                        matrice_column.append(matrice_line.copy())
                    elif matrix_column_expected is True:
                        raise SyntaxError()
                    elif value[0] == MATRICE_COLUMN_SEPARATOR:
                        value = value[1:]
                        matrix_column_expected = True
                        self.n += 1
                    else:
                        raise SyntaxError()

                self._value = matrice_column
            else:
                # Cannot create empty matrix.
                raise SyntaxError()

        except SyntaxError:
            raise SyntaxError(
                "An error occured when trying to create "
                + self.__class__.__name__
                + " object with the value : "
                + self._value
            )

    def __init__(self, value: str, pending_calc: bool = False):
        super().__init__()
        # Set to -1 before initializing the matrix value.
        self.n = -1
        self.m = -1
        self.value = value
        # pending_calc attribute is used to know if some calculation is unresolve inside the matrix.
        self.pending_calc = pending_calc

    def __str__(self) -> str:
        ret: str = "["
        first_column = True
        for column in self.value:
            if first_column:
                first_column = False
            else:
                ret += " ; "
            ret += "["
            first_line = True
            for line in column:
                if first_line:
                    first_line = False
                else:
                    ret += " , "
                for elem in line:
                    ret += str(elem)
            ret += "]"
        return ret + "]"

    def __repr__(self) -> str:
        return self.__class__.__name__ + "('" + str(self) + "')"


class Operator:
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value: str):
        self._value = value

    def __init__(self, value: str):
        if (
            len(value) == 1
            and value in "=?" + OPERATORS + SIGN + OPEN_PARENTHESES + CLOSING_PARENTHESES
        ):
            self.value = value
        else:
            raise SyntaxError(
                "An error occured when trying to create "
                + self.__class__.__name__
                + " object with the value : "
                + value
            )

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return self.__class__.__name__ + "('" + str(self) + "')"


class Function:
    _lock: bool = False

    def __init__(self, name: str, argument: str, right_expression: str = ""):
        if name.isalpha():
            self.name = name
            self.argument = argument
            self.right_expression = right_expression
        else:
            raise SyntaxError(
                "An error occured when trying to create "
                + self.__class__.__name__
                + " object with the name : "
                + name
                + " and the argument : "
                + argument
            )

    def __str__(self) -> str:
        return self.name + "('" + self.argument + "')"

    def __repr__(self) -> str:
        if len(self.right_expression) > 0:
            return (
                self.__class__.__name__
                + "("
                + self.name
                + "("
                + self.argument
                + ")"
                + "="
                + self.right_expression
                + ")"
            )
        else:
            return (
                self.__class__.__name__
                + "("
                + self.name
                + "("
                + self.argument
                + ")"
                + "="
                + "Not defined"
                + ")"
            )


class Variable:
    _lock: bool = False

    def __init__(self, name: str, value: list = None):
        super().__init__()
        if name.isalpha:
            self.name = name
            self.value = value
        else:
            raise SyntaxError(
                "An error occured when trying to create "
                + self.__class__.__name__
                + " object with the name : "
                + name
                + " and the value : "
                + str(value)
            )

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        if self.value is not None:
            return self.__class__.__name__ + "(" + self.name + " = " + self.value.__repr__() + ")"
        else:
            return self.__class__.__name__ + "(" + self.name + " = " + "Not defined" + ")"
