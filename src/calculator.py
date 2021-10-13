from math import cos, sin, atan

from typing import Union

from src.types.types import *
from src.types.types_utils import (
    sort_type_listed_expression_to_rpi,
    type_listed_expression_in_str,
)
from src.math_functions import my_power, my_round, my_sqrt, is_natural


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


class Calculator:
    def __init__(self, assigned_list: list):
        self._assigned_list = assigned_list

    def _real_calculator(self, elem_one: Real, elem_two: Real, operator: Operator) -> Real:
        """
        This method take two real type in input and an operator and return a real by resolving trivial calculation
        """

        print("Real calculator :") if self._verbose is True else None
        print(
            str(elem_one) + " " + str(operator) + " " + str(elem_two)
        ) if self._verbose is True else None

        if operator.value == "+":
            return Real(str(my_round(float(elem_one.value) + float(elem_two.value))))
        elif operator.value == "-":
            return Real(str(my_round(float(elem_one.value) - float(elem_two.value))))
        elif operator.value == "%":
            if float(elem_two.value) == 0.0:
                raise ValueError(
                    "The expression lead to a modulo zero : ",
                    str(elem_one),
                    " " + operator.value + " ",
                    str(elem_two),
                )
            return Real(str(my_round(float(elem_one.value) % float(elem_two.value))))

        elif operator.value == "/":
            if float(elem_two.value) == 0.0:
                raise ValueError(
                    "The expression lead to a division by zero : ",
                    str(elem_one),
                    " " + operator.value + " ",
                    str(elem_two),
                )
            return Real(str(my_round(float(elem_one.value) / float(elem_two.value))))
        elif operator.value == "*":
            return Real(str(my_round(float(elem_one.value) * float(elem_two.value))))
        elif operator.value == "^":
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
        print("Complex calculator :") if self._verbose is True else None
        print(
            str(elem_one) + " " + str(operator) + " " + str(elem_two)
        ) if self._verbose is True else None

        # Convert real into complex.
        if isinstance(elem_one, Real):
            elem_one = Complex(real_value=elem_one.value, imaginary_value=str(float(0.0)))
        if isinstance(elem_two, Real):
            elem_two = Complex(real_value=elem_two.value, imaginary_value=str(float(0.0)))

        if operator.value == "+":
            real_value = str(my_round(float(elem_one.real.value) + float(elem_two.real.value)))
            imaginary_value = str(
                my_round(float(elem_one.imaginary.value) + float(elem_two.imaginary.value))
            )
            return Complex(
                real_value=real_value,
                imaginary_value=imaginary_value,
            )
        elif operator.value == "-":
            real_value = str(my_round(float(elem_one.real.value) - float(elem_two.real.value)))
            imaginary_value = str(
                my_round(float(elem_one.imaginary.value) - float(elem_two.imaginary.value))
            )
            return Complex(
                real_value=real_value,
                imaginary_value=imaginary_value,
            )
        elif operator.value == "*":
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
        elif operator.value == "/":
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
                elem_one=elem_one, elem_two=conjugate_value, operator=Operator(value="*")
            )
            divider: Complex = self._complex_calculator(
                elem_one=elem_two, elem_two=conjugate_value, operator=Operator(value="*")
            )
            if float(divider.imaginary.value) != 0.0:
                raise Exception("Unexpected error when trying to resolve a division in complex.")
            real_value = str(float(dividend.real.value) / float(divider.real.value))
            imaginary_value = str(float(dividend.imaginary.value) / float(divider.real.value))
            return Complex(
                real_value=real_value,
                imaginary_value=imaginary_value,
            )
        elif operator.value == "%":
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
        elif operator.value == "^":
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
                    real_value=str(0.0),
                    imaginary_value=str(0.0),
                )
            if real_value == 0.0:
                # Simple multiplication loop.
                if natural_exponent > 0.0:
                    result = elem_one
                    i = 1
                    while i < natural_exponent:
                        result = self._complex_calculator(
                            elem_one=result, elem_two=elem_one, operator=Operator(value="*")
                        )
                        i += 1
                if natural_exponent < 0.0:
                    result = self._complex_calculator(
                        elem_one=Complex(
                            real_value="1.0",
                            imaginary_value="0.0",
                        ),
                        elem_two=elem_one,
                        operator=Operator(value="/"),
                    )
                    i = -1
                    while i > natural_exponent:
                        result = self._complex_calculator(
                            elem_one=result, elem_two=elem_one, operator=Operator(value="/")
                        )
                        i -= 1
                return result
            else:
                # Putting complex number to exponential form Z = rexp^{i a}
                # r is the module calculated following pytagore : c = sqrt(a^2 + b^2)
                r: float = my_sqrt(
                    my_power(number=real_value, power=2) + my_power(number=imaginary_value, power=2)
                )
                a = atan(imaginary_value / real_value)

                e = Complex(
                    real_value=str(cos(natural_exponent * a)),
                    imaginary_value=str(sin(natural_exponent * a)),
                )
                r = Complex(
                    real_value=str(my_power(number=r, power=natural_exponent)),
                    imaginary_value="0.0",
                )
                result = self._complex_calculator(
                    elem_one=r, elem_two=e, operator=Operator(value="*")
                )
                return result
        else:
            raise NotImplementedError(
                "Operator '" + operator.value + "' not implemented yet for complex.",
            )

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
                if calc_is_in_complex(elem_one=last_two_in_stack[0], elem_two=last_two_in_stack[1]):
                    result = self._complex_calculator(
                        elem_one=last_two_in_stack[0], elem_two=last_two_in_stack[1], operator=elem
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
        self._type_listed_expression = type_listed_expression

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
        return result
