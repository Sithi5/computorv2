import re

from globals_vars import (
    OPERATORS,
    SIGN,
    COMMA,
    OPEN_PARENTHESES,
    CLOSING_PARENTHESES,
    MATRICE_CLOSING_PARENTHESES,
    MATRICE_OPEN_PARENTHESES,
    MATRICE_COLUMN_SEPARATOR,
    MATRICE_LINE_SEPARATOR,
)

from src.math_functions import is_real


class BaseType:
    """Default class for Type. Should be used as an abstract class."""

    value: str = ""
    type: str

    def __init__(self):
        self.type = self.__class__.__name__

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return self.__class__.__name__ + "(" + self.value + ")"


class Real(BaseType):
    """
    Real type, the input value should be a real number.
    """

    def __init__(self, value: str):
        super().__init__()
        if is_real(value):
            self.value = value
        else:
            raise SyntaxError(
                "An error occured when trying to create "
                + self.__class__.__name__
                + " object with the value : "
                + value
            )


class Complex(BaseType):
    """
    Real type, the input value should be a complex number.
    Example:
    -   15i
    -   15.254i
    -   i
    """

    def __init__(self, value: str):
        super().__init__()
        if len(value) == 1 and value[0] == "i" or (value[-1] == "i" and is_real(value[:-1])):
            self.value = value
        else:
            raise SyntaxError(
                "An error occured when trying to create "
                + self.__class__.__name__
                + " object with the value : "
                + value
            )


class Matrice(BaseType):
    _n: int
    _m: int

    def __init__(self, value: str):
        self.value = value


class Function(BaseType):
    def __init__(self, name: str, argument: str, right_expression: str = ""):
        super().__init__()
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
        return self.name + "(" + self.argument + ")"

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


class Operator(BaseType):
    def __init__(self, value: str):
        super().__init__()
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


class Variable:
    _lock: bool = False

    def __init__(self, name: str, value: BaseType = None):
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