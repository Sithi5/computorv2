from typing import Union

from src.types.types import *
from src.types.types_utils import (
    sort_type_listed_expression_to_rpi,
    type_listed_expression_in_str,
)
from src.math_functions import my_power, my_round


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

        print("Real calculator :")
        print(elem_one)
        print(operator)
        print(elem_two)
        if operator.value == "+":
            return Real(str(my_round(float(elem_one.value) + float(elem_two.value))))
        elif operator.value == "-":
            return Real(str(my_round(float(elem_one.value) - float(elem_two.value))))
        elif operator.value == "%":
            if float(elem_two.value) == 0.0:
                raise ValueError(
                    "The expression lead to a modulo zero : ",
                    float(elem_one.value),
                    " " + operator.value + " ",
                    float(elem_two.value),
                )
            return Real(str(my_round(float(elem_one.value) % float(elem_two.value))))

        elif operator.value == "/":
            if float(elem_two.value) == 0.0:
                raise ValueError(
                    "The expression lead to a division by zero : ",
                    float(elem_one.value),
                    " " + operator.value + " ",
                    float(elem_two.value),
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
        print("Complex calculator :")
        print(elem_one)
        print(operator)
        print(elem_two)
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
        elif operator.value == "^":
            if float(elem_two.imaginary.value) != 0.0:
                raise NotImplementedError(
                    "Complex exponent is not implemented yet.",
                )
            exponent_real_number = float(elem_two.real.value)
            if exponent_real_number % 1 != 0:
                raise NotImplementedError(
                    "Complex exponent decimal numbers are not implemented yet.",
                )
            if exponent_real_number < 0:
                raise NotImplementedError(
                    "Complex exponent with negative value is not implemented yet.",
                )
            if float(elem_one.real.value) != 0.0:
                raise NotImplementedError(
                    "Calculate exponent for Complex with a real part is not implemented yet..",
                )
            real_value = str(float(0.0))
            if exponent_real_number > 0 and exponent_real_number % 4 == 0:
                exponent_real_number = 4.0
            elif exponent_real_number > 0:
                exponent_real_number = exponent_real_number % 4

            if exponent_real_number == 0:
                real_value = str(float(elem_one.imaginary.value))
                imaginary_value = str(float(0.0))
            if exponent_real_number == 1:
                imaginary_value = str(float(elem_one.imaginary.value))
            elif exponent_real_number == 2:
                real_value = str(float(elem_one.imaginary.value) * -1.0)
                imaginary_value = str(float(0.0))
            elif exponent_real_number == 3:
                imaginary_value = str(float(elem_one.imaginary.value) * -1.0)
            elif exponent_real_number == 4:
                imaginary_value = str(float(0.0))
                real_value = str(float(1.0))
            return Complex(
                real_value=real_value,
                imaginary_value=imaginary_value,
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
