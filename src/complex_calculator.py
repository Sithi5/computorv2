from typing import Union
from math import cos, sin, atan

from src.types.types import *
from src.globals_vars import *
from src.math_utils import my_power, my_round, my_sqrt, is_natural, PI


def complex_calculator(
    elem_one: Union[Real, Complex],
    elem_two: Union[Real, Complex],
    operator: Operator,
    verbose: bool = False,
) -> Complex:
    """
    This function take real/complex in input and an operator and return a complex number by resolving calculation.
    """

    print("\nComplex calculator :") if verbose is True else None
    print(
        "(" + str(elem_one) + ")" + " " + str(operator) + " " + "(" + str(elem_two) + ")" + "\n"
    ) if verbose is True else None

    # Convert real into complex.
    if isinstance(elem_one, Real):
        elem_one = Complex(real_value=elem_one.value, imaginary_value=str(float(0.0)))
    if isinstance(elem_two, Real):
        elem_two = Complex(real_value=elem_two.value, imaginary_value=str(float(0.0)))

    if not isinstance(elem_one, Complex) or not isinstance(elem_two, Complex):
        raise ValueError(
            """
            Wrong type in complex calculator. Input type should be:
            Real or Complex.
            """
        )

    if operator.value == ADDITION_SIGN:
        real_value = str(my_round(float(elem_one.real.value) + float(elem_two.real.value)))
        imaginary_value = str(
            my_round(float(elem_one.imaginary.value) + float(elem_two.imaginary.value))
        )
        return Complex(
            real_value=real_value,
            imaginary_value=imaginary_value,
        )
    elif operator.value == SUBSTRACTION_SIGN:
        real_value = str(my_round(float(elem_one.real.value) - float(elem_two.real.value)))
        imaginary_value = str(
            my_round(float(elem_one.imaginary.value) - float(elem_two.imaginary.value))
        )
        return Complex(
            real_value=real_value,
            imaginary_value=imaginary_value,
        )
    elif operator.value == MULTIPLICATION_SIGN:
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
    elif operator.value == DIVISION_SIGN:
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
        dividend: Complex = complex_calculator(
            elem_one=elem_one,
            elem_two=conjugate_value,
            operator=Operator(value=MULTIPLICATION_SIGN),
            verbose=verbose,
        )
        divider: Complex = complex_calculator(
            elem_one=elem_two,
            elem_two=conjugate_value,
            operator=Operator(value=MULTIPLICATION_SIGN),
            verbose=verbose,
        )
        if float(divider.imaginary.value) != 0.0:
            raise Exception("Unexpected error when trying to resolve a division in complex.")
        real_value = str(float(dividend.real.value) / float(divider.real.value))
        imaginary_value = str(float(dividend.imaginary.value) / float(divider.real.value))
        return Complex(
            real_value=real_value,
            imaginary_value=imaginary_value,
        )
    elif operator.value == MODULO_SIGN:
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
    elif operator.value == EXPONENT_SIGN:
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
                real_value=str(1.0),
                imaginary_value=str(0.0),
            )
        elif real_value == 0.0:
            # Imaginary only.
            powered_value = my_power(number=imaginary_value, power=natural_exponent)
            # The resulted i will loop over 4 case:
            # i ^ 1 = i
            # i ^ 2 = -1
            # i ^ 3 = -i
            # i ^ 4 = 1
            if natural_exponent % 4 == 0:
                result = Complex(
                    real_value=str(powered_value),
                    imaginary_value="0.0",
                )
            elif natural_exponent % 4 == 1:
                result = Complex(
                    real_value="0.0",
                    imaginary_value=str(powered_value),
                )
            elif natural_exponent % 4 == 2:
                result = Complex(
                    real_value=str(float(powered_value * -1.0)),
                    imaginary_value="0.0",
                )
            elif natural_exponent % 4 == 3:
                result = Complex(
                    real_value="0.0",
                    imaginary_value=str(float(powered_value * -1.0)),
                )
            return result
        else:
            # Putting complex number to exponential form Z = rexp^{i a}
            # r is the module calculated following pytagore : c = sqrt(a^2 + b^2)
            r: float = my_sqrt(
                my_power(number=real_value, power=2) + my_power(number=imaginary_value, power=2)
            )
            if real_value > 0.0:
                a = atan(imaginary_value / real_value)
            else:
                if imaginary_value >= 0.0:
                    a = atan(imaginary_value / real_value) + PI
                else:
                    a = atan(imaginary_value / real_value) - PI
            e = Complex(
                real_value=str(cos(natural_exponent * a)),
                imaginary_value=str(sin(natural_exponent * a)),
            )
            r = Complex(
                real_value=str(my_power(number=r, power=natural_exponent)),
                imaginary_value="0.0",
            )
            result = complex_calculator(
                elem_one=r,
                elem_two=e,
                operator=Operator(value=MULTIPLICATION_SIGN),
                verbose=verbose,
            )
            return result
    else:
        raise NotImplementedError(
            "Operator '" + operator.value + "' not implemented yet for complex.",
        )
