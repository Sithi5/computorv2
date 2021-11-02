from typing import Union

from src.types.types import *
from src.globals_vars import *
from src.calculators.real_calculator import real_calculator


def unresolved_calculator(
    elem_one: Union[BaseType, Unresolved, Function, Variable],
    elem_two: Union[BaseType, Unresolved, Function, Variable],
    operator: Operator,
    last_operator_priority_for_unresolved: int,
    verbose: bool = False,
) -> tuple():
    """
    This function take two Variable in input and do variable calculation.
    It return the resulted Unresolved type and the last_operator_priority_for_unresolved.
    """

    print("\nunresolved_calculator calculator :") if verbose is True else None
    print(
        str(elem_one) + " " + str(operator) + " " + str(elem_two) + "\n"
    ) if verbose is True else None

    if (
        not isinstance(elem_one, Unresolved)
        and not isinstance(elem_one, Variable)
        and not isinstance(elem_one, Function)
        and not isinstance(elem_two, Unresolved)
        and not isinstance(elem_two, Variable)
        and not isinstance(elem_two, Function)
    ):
        raise ValueError(
            """
            Wrong type in unresolved_calculator. Input type should be:
            Any type but at least one Unresolved/Variable/functions.
            """
        )
    first_elem_in_unresolved = None
    if isinstance(elem_one, Unresolved):
        unresolved = elem_one
        elem_in_stack = elem_two
    elif isinstance(elem_two, Unresolved):
        unresolved = elem_two
        elem_in_stack = elem_one
    else:
        unresolved = Unresolved()
        elem_in_stack = elem_two
        first_elem_in_unresolved = elem_one
    if (
        OPERATORS_PRIORITY[operator.value] > last_operator_priority_for_unresolved
        and len(unresolved) > 0
    ):
        unresolved.insert(0, Operator(value="("))
    if first_elem_in_unresolved:
        unresolved.append(first_elem_in_unresolved)
    if (
        OPERATORS_PRIORITY[operator.value] > last_operator_priority_for_unresolved
        and len(unresolved) > 3
    ):
        unresolved.append(Operator(value=")"))
    unresolved.append(operator)
    unresolved.append(elem_in_stack)
    last_operator_priority_for_unresolved = OPERATORS_PRIORITY[operator.value]
    return (unresolved, last_operator_priority_for_unresolved)
