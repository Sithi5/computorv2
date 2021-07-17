class BaseType:
    """Default class for Type. Should be used as an abstract class."""

    def __init__(self, value):
        self.value = value


class Real(BaseType):
    def __init__(self, name, value):
        super().__init__(name, value)


class Complex(BaseType):
    def __init__(self, name, value):
        super().__init__(name, value)


class Matrice(BaseType):
    _n: int
    _m: int

    def __init__(self, name, value):
        super().__init__(name, value)


class Function(BaseType):
    def __init__(self, name, value):
        super().__init__(name, value)
