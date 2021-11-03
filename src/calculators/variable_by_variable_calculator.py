from typing import Union

from src.types.types import *
from src.globals_vars import *
from src.calculators.real_calculator import real_calculator


def variable_by_variable_calculator(
    elem_one: Union[Variable, Real],
    elem_two: Union[Variable, Real],
    operator: Operator,
    verbose: bool = False,
) -> Variable:
    """
    This function take two Variable in input and do variable calculation.
    It return the resulted variable.
    """

    print("\nvariable_by_variable_calculator calculator :") if verbose is True else None
    print(
        str(elem_one) + " " + str(operator) + " " + str(elem_two) + "\n"
    ) if verbose is True else None

    if not isinstance(elem_one, Variable) or not isinstance(elem_two, Variable):
        raise ValueError(
            """
            Wrong type in variable_by_variable_calculator. Input type should be:
            Variables.
            """
        )
    if elem_one.name != elem_two.name:
        raise NotImplementedError(
            """
            Different variable calculation is not implemented yet.
        """
        )
    variable = elem_one
    if operator.value in ADDITION_SIGN + SUBSTRACTION_SIGN:
        if str(elem_one.exponent) != str(elem_two.exponent):
            raise NotImplementedError(
                """
            Cannot add or substract variable of different exponent for the moment.
            """
            )
        variable.coefficient = real_calculator(
            elem_one=variable.coefficient,
            elem_two=elem_two.coefficient,
            operator=operator,
        )
    elif operator.value == MULTIPLICATION_SIGN:
        variable.exponent = real_calculator(
            elem_one=variable.exponent, elem_two=elem_two.exponent, operator=Operator(ADDITION_SIGN)
        )
        variable.coefficient = real_calculator(
            elem_one=variable.coefficient,
            elem_two=elem_two.coefficient,
            operator=Operator(MULTIPLICATION_SIGN),
        )
    else:
        raise NotImplementedError(
            """
            Method not implemented yet.
            """
        )
    if float(str(variable.exponent)) == 0.0:
        return Real(value="1.0")
    if float(str(variable.coefficient)) == 0.0:
        return Real(value="0.0")
    return variable
