import copy

from typing import Union

from src.globals_vars import *
from src.types.types import *
from src.types.types_utils import (
    sort_type_listed_expression_to_rpi,
    convert_type_listed_expression_to_str,
    check_type_listed_expression_and_add_implicit_cross_operators,
)
from src.real_calculator import real_calculator
from src.complex_calculator import complex_calculator
from src.matrix_calculator import matrix_calculator
from src.variable_by_real_calculator import variable_by_real_calculator


def calc_is_in_complex(elem_one: BaseType, elem_two: BaseType) -> bool:
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


def calc_is_in_real(elem_one: BaseType, elem_two: BaseType) -> bool:
    """
    This method take two type in input and return true if the result of the calcul between those two type will be in Real.
    """
    return isinstance(elem_one, Real) and isinstance(elem_two, Real)


def calc_is_var_by_var(elem_one: BaseType, elem_two: BaseType) -> bool:
    """
    This method take two type in input and return true if both element are Variable.
    """
    return isinstance(elem_one, Variable) and isinstance(elem_two, Variable)


def calc_is_in_var_or_function_or_unresolved(elem_one: BaseType, elem_two: BaseType) -> bool:
    """
    This method take two type in input and return true if at least one element is variable/function/Unresolved type.
    """
    return isinstance(elem_one, Variable) and isinstance(elem_two, Variable)


def calc_is_var_multiply_or_exponent_by_real(
    elem_one: BaseType, elem_two: BaseType, operator: Operator
) -> bool:
    """
    This method take two type in input and return true if it imply a multiplication between a var and a real or a real exponent to a var.
    """

    return (
        (
            (isinstance(elem_one, Real) and isinstance(elem_two, Variable))
            or (isinstance(elem_two, Real) and isinstance(elem_one, Variable))
        )
        and operator.value in MULTIPLICATION_SIGN + DIVISION_SIGN
        or (
            isinstance(elem_two, Real)
            and isinstance(elem_one, Variable)
            and operator.value == EXPONENT_SIGN
        )
    )


def calc_is_in_matrice(elem_one: BaseType, elem_two: BaseType) -> bool:
    """
    This method take two type in input and return true if the result of the calcul between those two type will be a matrix type.
    """
    return isinstance(elem_one, Matrix) or isinstance(elem_two, Matrix)


class Calculator:
    def __init__(self, assigned_list: list):
        self._assigned_list = assigned_list

    def _resolve_inside_matrice(self, matrix: Matrix) -> Matrix:
        if isinstance(matrix, Matrix) and matrix.pending_calculation:

            print("\nResolve_inside_matrice :") if self._verbose is True else None
            print(str(matrix) + "\n") if self._verbose is True else None

            for column in matrix.value:
                for row in column:
                    row_save = row.copy()
                    row.clear()
                    old_type_listed_expression = self._type_listed_expression
                    row.append(
                        self.solve(
                            type_listed_expression=check_type_listed_expression_and_add_implicit_cross_operators(
                                type_listed_expression=row_save
                            ),
                            verbose=self._verbose,
                        )
                    )
                    self._type_listed_expression = old_type_listed_expression
            matrix.pending_calculation = False
        return matrix

    def _resolve_rpi_type_listed_expression(self) -> Union[BaseType, Unresolved]:
        """
        This method resolve a type_listed_expression and return the result with the correct type.
        """
        stack = []
        result: BaseType
        last_operator_priority_for_unresolved = OPERATORS_MINIMAL_PRIORITY

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
                elem_one = last_two_in_stack[0]
                elem_two = last_two_in_stack[1]
                operator = elem

                # CALC WITH VAR/FUNCTION/UNRESOLVER, REDUCE FORM FOR UNRESOLVED CALC
                if (
                    isinstance(elem_one, Variable)
                    or isinstance(elem_one, Function)
                    or isinstance(elem_one, Unresolved)
                    or isinstance(elem_two, Variable)
                    or isinstance(elem_two, Function)
                    or isinstance(elem_two, Unresolved)
                ):
                    if calc_is_var_multiply_or_exponent_by_real(
                        elem_one=elem_one, elem_two=elem_two, operator=operator
                    ):
                        # VAR BY REAL
                        result = variable_by_real_calculator(
                            elem_one=elem_one,
                            elem_two=elem_two,
                            operator=operator,
                            verbose=self._verbose,
                        )
                        # END OF VAR BY REAL
                    # elif calc_is_var_by_var(elem_one=elem_one, elem_two=elem_two):
                    #     # VAR BY VAR CALCULATION
                    #     pass
                    #     # END OF VAR BY VAR CALCULATION
                    else:
                        # REDUCED FORM
                        if self._reduce_form_allowed is False:
                            raise ValueError(
                                "No reduce form allowed for this non resolved expression."
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
                            OPERATORS_PRIORITY[operator.value]
                            > last_operator_priority_for_unresolved
                            and len(unresolved) > 0
                        ):
                            unresolved.insert(0, Operator(value="("))
                        if first_elem_in_unresolved:
                            unresolved.append(first_elem_in_unresolved)
                        if (
                            OPERATORS_PRIORITY[operator.value]
                            > last_operator_priority_for_unresolved
                            and len(unresolved) > 3
                        ):
                            unresolved.append(Operator(value=")"))
                        unresolved.append(operator)
                        unresolved.append(elem_in_stack)
                        last_operator_priority_for_unresolved = OPERATORS_PRIORITY[operator.value]
                        result = unresolved
                        # END OF REDUCED FORM
                # END OF CALC WITH VAR/FUNCTION/UNRESOLVER, REDUCE FORM FOR UNRESOLVED CALC

                # REAL CALC
                elif calc_is_in_real(elem_one=elem_one, elem_two=elem_two):
                    result = real_calculator(
                        elem_one=elem_one,
                        elem_two=elem_two,
                        operator=operator,
                        verbose=self._verbose,
                    )
                # END OF REAL CALC

                # COMPLEX CALC
                elif calc_is_in_complex(elem_one=elem_one, elem_two=elem_two):
                    result = complex_calculator(
                        elem_one=elem_one,
                        elem_two=elem_two,
                        operator=operator,
                        verbose=self._verbose,
                    )
                # END OF COMPLEX CALC

                # MATRIX CALC
                elif calc_is_in_matrice(elem_one=elem_one, elem_two=elem_two):
                    if isinstance(elem_one, Matrix):
                        elem_one = self._resolve_inside_matrice(matrix=elem_one)
                    if isinstance(elem_two, Matrix):
                        elem_two = self._resolve_inside_matrice(matrix=elem_two)
                    result = matrix_calculator(
                        elem_one=elem_one,
                        elem_two=elem_two,
                        operator=operator,
                        verbose=self._verbose,
                    )
                # END OF MATRIX CALC
                else:
                    raise Exception(
                        "Unexpected error when trying to resolve npi. Maybe your input format is not accepted?"
                    )
                stack.append(result)

        if len(stack) > 1:
            raise Exception(
                "Unexpected error when trying to resolve npi. Maybe your input format is not accepted?"
            )

        return stack[0]

    def _resolve_variables_and_functions(self):
        """
        Resolve all variables and functions from a type listed expression to their respective value.
        Raise a ValueError if couln't resolve.
        Return the new type_listed_expression.
        """

        def _get_variable_value(variable: Variable) -> BaseType:
            """
            This function return the saved value of a variable.
            """
            assigned_list = copy.deepcopy(self._assigned_list)
            for elem in assigned_list:
                if variable.name == elem.name:
                    return elem.value
            raise ValueError("Couln't resolve the variable : ", variable)

        def _get_function_value(function: Function) -> list:
            """
            This function return the saved value of a function.
            """
            assigned_list = copy.deepcopy(self._assigned_list)
            for elem in assigned_list:
                if function.name == elem.name:
                    return elem.value
            raise ValueError("Couln't resolve the function : ", function)

        def _resolve_variable_value(variable_value: BaseType, variable: Variable) -> BaseType:
            """
            This function resolve a variable to get the value after calculating the coefficient and the exponent.
            """
            type_listed_expression = []
            type_listed_expression.append(variable_value)
            type_listed_expression.append(Operator(MULTIPLICATION_SIGN))
            type_listed_expression.append(variable.coefficient)
            type_listed_expression.append(Operator(EXPONENT_SIGN))
            type_listed_expression.append(variable.exponent)
            old_type_listed_expression = self._type_listed_expression
            ret = self.solve(type_listed_expression=type_listed_expression, verbose=self._verbose)
            self._type_listed_expression = old_type_listed_expression
            return ret

        def _resolve_function_value(function: Function) -> list:
            """
            This function resolve the value of a function by resolving all the var.
            """
            if isinstance(function.argument, Variable):
                function_variable_value = _get_variable_value(variable=function.argument)
            elif isinstance(function.argument, Real):
                function_variable_value = function.argument
            else:
                raise ValueError("Couln't resolve the function : ", str(function))
            function_variable_name = None
            assigned_list = copy.deepcopy(self._assigned_list)
            for elem in assigned_list:
                if str(function.name) == str(elem.name):
                    function_variable_name = elem.argument.name[:]
                    function.value = elem.value

            if not function.value or not function_variable_name:
                raise ValueError("Couln't resolve the function : ", str(function))
            else:
                for index, elem in enumerate(function.value):
                    if isinstance(elem, Variable) and elem.name == function_variable_name:
                        function.value[index] = _resolve_variable_value(
                            variable_value=function_variable_value, variable=elem
                        )

            old_type_listed_expression = self._type_listed_expression
            ret = self.solve(type_listed_expression=function.value, verbose=self._verbose)
            self._type_listed_expression = old_type_listed_expression
            return ret

        type_listed_expression = copy.deepcopy(self._type_listed_expression)
        value_error: str = ""

        for index, elem in enumerate(type_listed_expression):
            try:
                if isinstance(elem, Variable):
                    self._type_listed_expression[index] = _resolve_variable_value(
                        variable_value=_get_variable_value(variable=elem), variable=elem
                    )
                elif isinstance(elem, Function):
                    elem.value = _get_function_value(function=elem)
                    if isinstance(elem.argument, Variable):
                        try:
                            self._type_listed_expression[index] = _resolve_function_value(
                                function=elem
                            )
                        except:
                            self._type_listed_expression[index] = elem.value
                    else:
                        self._type_listed_expression[index] = _resolve_function_value(function=elem)
            except ValueError as e:
                if value_error == "":
                    value_error = str(e)
                else:
                    value_error += " and " + str(e)
        if value_error != "":
            raise ValueError(value_error)

    def solve(
        self,
        type_listed_expression: list,
        verbose: bool = False,
        reduce_form_allowed: bool = True,
        *arg,
        **kwarg
    ) -> Union[BaseType, Unresolved]:
        """
        Resolving calcul from one part type_listed_expression.
        If the reduce_form_allowed is set to true, it will try to reduce as much as possible expression even with unknow vars.
        """
        self._verbose = verbose
        self._type_listed_expression = type_listed_expression
        self._reduce_form_allowed = reduce_form_allowed
        print(
            "\nResolving following type_listed_expression : ", self._type_listed_expression
        ) if self._verbose is True else None

        if self._verbose:
            print("Assigned list: ")
            for elem in self._assigned_list.copy():
                print(elem.name, " = ", elem.value)

        try:
            self._resolve_variables_and_functions()
        except ValueError as e:
            if reduce_form_allowed == False:
                raise ValueError(e)

        print(
            "Converting var and function to their respective value : ", self._type_listed_expression
        ) if self._verbose is True else None

        self._type_listed_expression = sort_type_listed_expression_to_rpi(
            type_listed_expression=self._type_listed_expression
        )
        print(
            "\nExpression in RPI: ",
            convert_type_listed_expression_to_str(
                type_listed_expression=self._type_listed_expression
            ),
        ) if self._verbose is True else None

        result: Union[BaseType, Unresolved] = self._resolve_rpi_type_listed_expression()

        if isinstance(result, Matrix):
            # Check for unresolved matrix and resolve it.
            result = self._resolve_inside_matrice(matrix=result)
        if isinstance(result, Unresolved) and not reduce_form_allowed:
            raise ValueError("One of the variable/function have an unknow value.")

        print(
            "\nResult at end of calculator: ",
            str(result),
        ) if self._verbose is True else None
        return result
