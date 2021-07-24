import re

from computorv2.globals_vars import (
    OPERATORS,
    SIGN,
    OPEN_PARENTHESES,
    CLOSING_PARENTHESES,
)

from computorv2.src.math_functions import is_real


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
        return self.__class__.__name__ + "('" + self.value + "')"


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


class Complex(BaseType):
    """
    Real type, the input value should be a complex number.
    Example:
    -   15i
    -   15.254i
    -   i
    """

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value: str):
        if len(value) == 1 and value[0] == "i" or (value[-1] == "i" and is_real(value[:-1])):
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
        return self.__class__.__name__ + "('" + self.value + "')"


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