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

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return self.__class__.__name__ + "(" + self.value + ")"


class Real(BaseType):
    """
    Real type, the input value should be a real number.
    """

    def __init__(self, value: str):
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
    """
    Function type, the input value should be in the format : 'NameOfTheFunction'.upper() + '(' + 'Value/Variable' + ')'
    """

    def __init__(self, value: str):
        regex_functions = re.compile(rf"[A-Z]+\([\d\{COMMA}A-Z]+\)")
        if regex_functions.fullmatch(string=value):
            self.value = value
        else:
            raise SyntaxError(
                "An error occured when trying to create "
                + self.__class__.__name__
                + " object with the value : "
                + value
            )


class Operator(BaseType):
    def __init__(self, value: str):
        if (
            len(value) == 1
            and value in "=" + OPERATORS + SIGN + OPEN_PARENTHESES + CLOSING_PARENTHESES
        ):
            self.value = value
        else:
            raise SyntaxError(
                "An error occured when trying to create "
                + self.__class__.__name__
                + " object with the value : "
                + value
            )
