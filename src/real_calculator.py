from src.types.types import *
from src.globals_vars import *
from src.math_utils import my_power, my_round, is_natural


def real_calculator(
    elem_one: Real, elem_two: Real, operator: Operator, verbose: bool = False
) -> Real:
    """
    This function take two real type in input and an operator and return a real by resolving trivial calculation.
    """

    print("\nReal calculator :") if verbose is True else None
    print(
        str(elem_one) + " " + str(operator) + " " + str(elem_two) + "\n"
    ) if verbose is True else None

    if not isinstance(elem_one, Real) or not isinstance(elem_two, Real):
        raise ValueError(
            """
            Wrong type in real calculator. Input type should be:
            Real.
            """
        )

    if operator.value == ADDITION_SIGN:
        return Real(str(my_round(float(elem_one.value) + float(elem_two.value))))
    elif operator.value == SUBSTRACTION_SIGN:
        return Real(str(my_round(float(elem_one.value) - float(elem_two.value))))
    elif operator.value == MODULO_SIGN:
        if float(elem_two.value) == 0.0:
            raise ValueError(
                "The expression lead to a modulo zero : ",
                str(elem_one),
                " " + operator.value + " ",
                str(elem_two),
            )
        return Real(str(my_round(float(elem_one.value) % float(elem_two.value))))

    elif operator.value == DIVISION_SIGN:
        if float(elem_two.value) == 0.0:
            raise ValueError(
                "The expression lead to a division by zero : ",
                str(elem_one),
                " " + operator.value + " ",
                str(elem_two),
            )
        return Real(str(my_round(float(elem_one.value) / float(elem_two.value))))
    elif operator.value == MULTIPLICATION_SIGN:
        return Real(str(my_round(float(elem_one.value) * float(elem_two.value))))
    elif operator.value == EXPONENT_SIGN:
        if not is_natural(n=elem_two.value):
            raise NotImplementedError("Exponent should be natural for the moment.")
        return Real(str(my_round(my_power(float(elem_one.value), int(float(elem_two.value))))))
    else:
        raise ValueError(
            "The expression operator is unknown : ",
            operator.value,
        )
