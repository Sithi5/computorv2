class BaseType:
    """Default class for Type. Should be used as an abstract class."""

    def __init__(self, value: str):
        self.value = value

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return self.__class__.__name__ + "(" + self.value + ")"


class Real(BaseType):
    def __init__(self, value):
        super().__init__(value)


class Complex(BaseType):
    def __init__(self, value):
        super().__init__(value)


class Matrice(BaseType):
    _n: int
    _m: int

    def __init__(self, value):
        super().__init__(value)


class Function(BaseType):
    def __init__(self, value):
        super().__init__(value)
