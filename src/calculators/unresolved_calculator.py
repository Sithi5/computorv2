import copy

from typing import Union
from src.calculators.real_calculator import real_calculator
from src.calculators.complex_calculator import complex_calculator
from src.calculators.variable_by_variable_calculator import variable_by_variable_calculator

from src.types.types import *
from src.globals_vars import *


def insert_inside_unresolved(
    unresolved: Unresolved,
    operator: Operator,
    new_elem: Union[BaseType, Variable, Function, Unresolved],
) -> bool:
    """
    This function try to insert the new element inside the Unresolved class by simplifying it if possible.
    Return true if it succeed or false if not.
    example :
    Unresolved = 10 + X
    operator = +
    new_elem = 18
    result : 28 + X instead of 10 + X + 18.
    """
    if OPERATORS_PRIORITY[operator.value] == OPERATORS_MINIMAL_PRIORITY and (
        isinstance(new_elem, Real)
        or isinstance(new_elem, Complex)
        or isinstance(new_elem, Variable)
    ):
        # Here trying to insert and simplify our element with element inside the Unresolved.
        for index, elem in enumerate(unresolved):
            if (
                (isinstance(elem, Real) or isinstance(elem, Complex))
                and (
                    isinstance(new_elem, Real) or isinstance(new_elem, Complex)
                )  # Real or complex match
            ) or (
                isinstance(elem, Variable)
                and isinstance(new_elem, Variable)
                and elem.name == new_elem.name
            ):  # Variables match
                if index == 0:
                    previous_operator_priority = OPERATORS_MINIMAL_PRIORITY
                else:
                    if unresolved[index - 1].value in CLOSING_PARENTHESES + OPENING_PARENTHESES:
                        previous_operator_priority = OPERATORS_MAXIMAL_PRIORITY
                    else:
                        previous_operator_priority = OPERATORS_PRIORITY[unresolved[index - 1].value]
                if index == len(unresolved) - 1:
                    next_operator_priority = OPERATORS_MINIMAL_PRIORITY
                else:
                    if unresolved[index + 1].value in CLOSING_PARENTHESES + OPENING_PARENTHESES:
                        previous_operator_priority = OPERATORS_MAXIMAL_PRIORITY
                    else:
                        next_operator_priority = OPERATORS_PRIORITY[unresolved[index + 1].value]
                if (
                    previous_operator_priority == OPERATORS_MINIMAL_PRIORITY
                    and next_operator_priority == OPERATORS_MINIMAL_PRIORITY
                ):
                    if isinstance(elem, Complex) or isinstance(new_elem, Complex):
                        unresolved[index] = complex_calculator(
                            elem_one=unresolved[index],
                            elem_two=new_elem,
                            operator=operator,
                            verbose=False,
                        )
                    elif isinstance(elem, Variable) and isinstance(new_elem, Variable):
                        try:
                            ret = variable_by_variable_calculator(
                                elem_one=unresolved[index],
                                elem_two=new_elem,
                                operator=operator,
                                verbose=False,
                            )
                            unresolved[index] = ret
                        except NotImplementedError:
                            continue
                    else:
                        unresolved[index] = real_calculator(
                            elem_one=unresolved[index],
                            elem_two=new_elem,
                            operator=operator,
                            verbose=False,
                        )
                    return True
                    break
    return False


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
        new_elem = elem_two
    elif isinstance(elem_two, Unresolved):
        unresolved = elem_two
        new_elem = elem_one
    else:
        unresolved = Unresolved()
        new_elem = elem_two
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

    if not insert_inside_unresolved(unresolved=unresolved, operator=operator, new_elem=new_elem):
        unresolved.append(operator)
        unresolved.append(new_elem)

    last_operator_priority_for_unresolved = OPERATORS_PRIORITY[operator.value]
    return (unresolved, last_operator_priority_for_unresolved)
