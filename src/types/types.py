from src.globals_vars import (
    OPERATORS,
    SIGN,
    OPEN_PARENTHESES,
    CLOSING_PARENTHESES,
)

from src.math_functions import is_real, my_round, my_abs


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
            return str(self.imaginary) + "i"
        elif float(self.imaginary.value) == 0.0:
            return str(self.real)
        else:
            if float(self.imaginary.value) > 0.0:
                return str(self.real) + " + " + str(self.imaginary) + "i"
            else:
                return str(self.real) + " - " + str(my_abs(float(self.imaginary.value))) + "i"

    def __repr__(self) -> str:
        return self.__class__.__name__ + "('" + str(self) + "')"


class Matrice(BaseType):
    _n: int
    _m: int

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value: str):
        self._value = value

    def __init__(self, value: str):
        super().__init__()
        self.value = value


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
