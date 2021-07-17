from src.types.types import BaseType


class Variable:
    _lock: bool = False

    def __init__(self, name: str, value: BaseType):
        self.name = name
        self.value = value

    def __str__(self) -> str:
        return self.name + " = " + str(self.value)

    def __repr__(self) -> str:
        return self.__class__.__name__ + "(" + self.name + " = " + str(self.value) + ")"
