class BaseType:
    """Default class for variable Type. Should be used as an abstract class."""

    _lock: bool = False

    def __init__(self, name, value):
        self.name: str = name
        self.value = value

    def __str__(self) -> str:
        return self.name + " = " + str(self.value)

    def __repr__(self) -> str:
        return self.__class__.__name__ + "(" + self.name + " = " + str(self.value) + ")"


class Real(BaseType):
    def __init__(self, name, value):
        super().__init__(name, value)


class Complex(BaseType):
    def __init__(self, name, value):
        super().__init__(name, value)


class Matrice(BaseType):
    def __init__(self, name, value):
        super().__init__(name, value)


class Function(BaseType):
    def __init__(self, name, value):
        super().__init__(name, value)