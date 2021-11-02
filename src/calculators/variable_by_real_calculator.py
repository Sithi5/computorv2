from typing import Union

from src.types.types import *
from src.globals_vars import *
from src.calculators.real_calculator import real_calculator


def variable_by_real_calculator(
    elem_one: Union[Variable, Real],
    elem_two: Union[Variable, Real],
    operator: Operator,
    verbose: bool = False,
) -> Union[Variable, Real]:
    """
    This function take one Variable and one Real in input and do variable calculation.
    It return the resulted variable or a real in some case.
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
        if float(real.value) == 0.0:
            return Real(value="1.0")
        elif float(variable.exponent.value) == 1.0:
            # TODO not sure of this.
            variable.exponent = real
        else:
            variable.exponent = real_calculator(
                elem_one=real,
                elem_two=variable.exponent,
                operator=operator,
                verbose=verbose,
            )
    elif operator.value in MULTIPLICATION_SIGN + DIVISION_SIGN:
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
    elif (
        operator.value == SUBSTRACTION_SIGN
        and isinstance(elem_one, Real)
        and float(elem_one.value) == 0.0
    ):
        variable.coefficient = real_calculator(
            elem_one=variable.coefficient,
            elem_two=Real(value="-1.0"),
            operator=Operator(value=MULTIPLICATION_SIGN),
            verbose=verbose,
        )
    else:
        raise NotImplementedError(
            """
        This operations with variable is not implemented yet.
        """
        )
    return variable
