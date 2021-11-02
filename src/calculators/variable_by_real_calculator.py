from typing import Union

from src.types.types import *
from src.globals_vars import *
from src.calculators.real_calculator import real_calculator


def variable_by_real_calculator(
    elem_one: Union[Variable, Real],
    elem_two: Union[Variable, Real],
    operator: Operator,
    verbose: bool = False,
) -> Variable:
    """
    This function take one Variable and one Real in input and do variable calculation.
    It return the resulted variable.
    """

    print("\nvariable_by_real_calculator calculator :") if verbose is True else None
    print(
        str(elem_one) + " " + str(operator) + " " + str(elem_two) + "\n"
    ) if verbose is True else None

    if (not isinstance(elem_one, Variable) and not isinstance(elem_two, Variable)) or (
        not isinstance(elem_one, Real) and not isinstance(elem_two, Real)
    ):
        raise ValueError(
            """
            Wrong type in variable_by_real_calculator. Input type should be:
            Real and Variable.
            """
        )

    if isinstance(elem_one, Variable):
        variable = elem_one
        real = elem_two
    else:
        variable = elem_two
        real = elem_one
    if operator.value == EXPONENT_SIGN:
        # TODO not sure of this.
        if variable.exponent.value == "1.0":
            variable.exponent = real
        else:
            variable.exponent = real_calculator(
                elem_one=real,
                elem_two=variable.exponent,
                operator=operator,
                verbose=verbose,
            )
    else:
        if isinstance(elem_one, Variable):
            variable.coefficient = real_calculator(
                elem_one=variable.coefficient,
                elem_two=real,
                operator=operator,
                verbose=verbose,
            )
        else:
            variable.coefficient = real_calculator(
                elem_one=real,
                elem_two=variable.coefficient,
                operator=operator,
                verbose=verbose,
            )
    return variable
