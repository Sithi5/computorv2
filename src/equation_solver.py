# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    equation_solver.py                                 :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: mabouce <ma.sithis@gmail.com>              +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/12/01 20:27:27 by mabouce           #+#    #+#              #
#    Updated: 2021/07/24 16:41:34 by mabouce          ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import re

from src.globals_vars import *
from src.types.types import Function, Operator, Real, Unresolved, Variable

from src.utils import (
    convert_signed_number,
    parse_sign,
    get_var_multiplier,
    add_implicit_cross_operator_for_vars,
)

from src.types.types_utils import (
    convert_expression_to_type_list,
    check_type_listed_expression_and_add_implicit_cross_operators,
)

from src.math_utils import my_power, my_round, my_sqrt, is_natural

from src.calculators.calculator import Calculator


class EquationSolver:
    _left_part: list = []
    _right_part: list = []

    def __init__(self, calculator: Calculator, output_graph: bool = False):
        self._calculator = calculator
        self._output_graph = output_graph

    def _check_have_var(self, var) -> bool:
        if self._var_name in var:
            return True
        return False

    def _get_power(self, var):
        """
        Returning the power of a number or a var.
        If there is multiple "^" operators, it return the first power.
        """
        split = var.split("^")
        if len(split) == 1:
            return 1.0
        else:
            return float(split[1])

    def _get_polynom_dict(self, simplified_part: str) -> dict:
        polynom_dict = {}
        index = 0
        part = ""
        sign = "+"
        while index < len(simplified_part):
            if simplified_part[index] in SIGN and len(part) > 0:
                if self._check_have_var(part):
                    power = self._get_power(part)
                    if power == 1:
                        polynom_dict["b"] = (
                            SUBSTRACTION_SIGN + part if sign == SUBSTRACTION_SIGN else part
                        )
                    elif power == 2:
                        polynom_dict["a"] = (
                            SUBSTRACTION_SIGN + part if sign == SUBSTRACTION_SIGN else part
                        )
                    else:
                        polynom_dict[str(power)] = (
                            SUBSTRACTION_SIGN + part if sign == SUBSTRACTION_SIGN else part
                        )
                else:
                    polynom_dict["c"] = (
                        SUBSTRACTION_SIGN + part if sign == SUBSTRACTION_SIGN else part
                    )
                part = ""
            if simplified_part[index] in SIGN:
                sign = simplified_part[index]
            else:
                part = part + simplified_part[index]
            index += 1
        if self._check_have_var(part):
            power = self._get_power(part)
            if power == 1:
                polynom_dict["b"] = SUBSTRACTION_SIGN + part if sign == SUBSTRACTION_SIGN else part
            elif power == 2:
                polynom_dict["a"] = SUBSTRACTION_SIGN + part if sign == SUBSTRACTION_SIGN else part
            else:
                polynom_dict[str(power)] = (
                    SUBSTRACTION_SIGN + part if sign == SUBSTRACTION_SIGN else part
                )
        else:
            polynom_dict["c"] = SUBSTRACTION_SIGN + part if sign == SUBSTRACTION_SIGN else part
        return polynom_dict

    def _push_right_to_left(self):
        for key, right_value in self._polynom_dict_right.items():
            try:
                left_value = self._polynom_dict_left[key]
            except:
                left_value = 0.0

            print("_push_right_to_left")
            print("right_value = ", right_value)
            print("left_value = ", left_value)
            type_listed_expression = check_type_listed_expression_and_add_implicit_cross_operators(
                convert_expression_to_type_list(
                    expression=convert_signed_number(
                        parse_sign(
                            add_implicit_cross_operator_for_vars(
                                list(self._var_name), str(left_value)
                            )
                            + SUBSTRACTION_SIGN
                            + add_implicit_cross_operator_for_vars(
                                list(self._var_name), str(right_value)
                            )
                        ),
                        accept_var=True,
                    )
                )
            )
            print("type_listed_expression = ", type_listed_expression)
            ret = self._calculator.solve(
                type_listed_expression=type_listed_expression,
                verbose=self._force_calculator_verbose,
            )
            print("ret =", ret)
            self._polynom_dict_left[key] = ret.value

    def _check_polynom_degree(self):
        polynom_max_degree = 0.0
        for key, value in self._polynom_dict_left.items():
            if key == "a":
                if self._var_name in value and polynom_max_degree < 2:
                    polynom_max_degree = float(2)
                else:
                    continue
            elif key == "b":
                if self._var_name in value and polynom_max_degree < 1:
                    polynom_max_degree = float(1)
                else:
                    continue
            elif key == "c":
                continue
            elif float(key) > 2 and self._var_name in value and polynom_max_degree < float(key):
                polynom_max_degree = float(key)
        self._polynom_degree = polynom_max_degree

    def _get_discriminant(self, a: float, b: float, c: float) -> float:
        return my_power(b, 2) - 4.0 * a * c

    def _solve_polynom_degree_two(self):
        try:
            a = get_var_multiplier(self._polynom_dict_left["a"], var_name=self._var_name)
        except:
            a = 0.0
        try:
            b = get_var_multiplier(self._polynom_dict_left["b"], var_name=self._var_name)
        except:
            b = 0.0
        try:
            c = float(self._polynom_dict_left["c"])
        except:
            c = 0.0

        print("a = ", a, " b = ", b, " c = ", c) if self._verbose is True else None

        discriminant = self._get_discriminant(a, b, c)
        if discriminant > 0:
            print("The discriminant is strictly positive.") if self._verbose is True else None
        elif discriminant == 0:
            print("The discriminant is exactly zero.") if self._verbose is True else None
        else:
            print("The discriminant is strictly negative.") if self._verbose is True else None
        print("discriminant = ", discriminant) if self._verbose is True else None
        if discriminant > 0:
            self.solution = []
            if a == 0:
                raise ValueError(
                    "The expression lead to a division by zero : ",
                    float(str((-b + my_sqrt(discriminant)))),
                    " / ",
                    a,
                )
            solution_one = str((-b + my_sqrt(discriminant)) / (2 * a))
            solution_two = str((-b - my_sqrt(discriminant)) / (2 * a))
            if solution_one == "-0.0":
                solution_one = "0.0"
            if solution_two == "-0.0":
                solution_two = "0.0"
            self.solution.append(str(my_round(float(solution_one), 6)))
            self.solution.append(str(my_round(float(solution_two), 6)))
        elif discriminant == 0:
            if a == 0:
                raise ValueError(
                    "The expression lead to a division by zero : ",
                    float(str((-b + my_sqrt(discriminant)))),
                    " / ",
                    a,
                )
            self.solution = str((-b) / (2 * a))
            if self.solution == "-0.0":
                self.solution = "0.0"
        else:
            print("There is two solutions in complex number.") if self._verbose is True else None
            self.solution = []
            discriminant = -discriminant
            solution_one = convert_signed_number(
                f"{-b} / (2 * {a}) + i * {my_sqrt(discriminant)} / (2 * {a})".replace(" ", "")
            )
            type_listed_expression = check_type_listed_expression_and_add_implicit_cross_operators(
                convert_expression_to_type_list(
                    expression=convert_signed_number(parse_sign(solution_one), accept_var=True)
                )
            )
            ret = self._calculator.solve(
                type_listed_expression=type_listed_expression,
                verbose=self._force_calculator_verbose,
            )
            self.solution.append(str(ret))

            solution_two = f"{-b} / (2 * {a}) - i * {my_sqrt(discriminant)} / (2 * {a})".replace(
                " ", ""
            )

            type_listed_expression = check_type_listed_expression_and_add_implicit_cross_operators(
                convert_expression_to_type_list(
                    expression=convert_signed_number(parse_sign(solution_two), accept_var=True)
                )
            )
            ret = self._calculator.solve(
                type_listed_expression=type_listed_expression,
                verbose=self._force_calculator_verbose,
            )
            self.solution.append(str(ret))

    def _solve_polynom_degree_one(self):
        try:
            b = get_var_multiplier(self._polynom_dict_left["b"], var_name=self._var_name)
        except:
            b = 0.0
        try:
            c = float(self._polynom_dict_left["c"])
        except:
            c = 0.0

        print("b = ", b, " c = ", c) if self._verbose is True else None
        if b != 0.0:
            self.solution = str(-(c / b))
        else:
            if b != c:
                self.solution = "There is no solution for this equation."
            else:
                self.solution = "X can be any real number."
        if self.solution == "-0.0":
            self.solution = "0.0"

    def _reducing_form(self):
        self._reduced_form = ""
        a, b, c = "0.0", "0.0", "0.0"
        for key, value in self._polynom_dict_left.items():
            if key == "a":
                a = value
            elif key == "b":
                b = value
            else:
                c = value
        if a != "0.0":
            self._reduced_form = a
        if b != "0.0":
            self._reduced_form = self._reduced_form + "+" + b
        if c != "0.0":
            self._reduced_form = self._reduced_form + "+" + c

        if len(self._reduced_form) == 0:
            self._reduced_form = "0.0"
        self._reduced_form = parse_sign(self._reduced_form) + "=0.0"

        print("Reduced form : ", self._reduced_form) if self._verbose is True else None

    def _create_graph_file(self, graph_name: str = "equation_graph"):
        import matplotlib.pyplot as plt  # type: ignore

        try:
            a = get_var_multiplier(self._polynom_dict_left["a"], var_name=self._var_name)
        except:
            a = 0.0
        try:
            b = get_var_multiplier(self._polynom_dict_left["b"], var_name=self._var_name)
        except:
            b = 0.0
        try:
            c = float(self._polynom_dict_left["c"])
        except:
            c = 0.0

        x = [i - 50 for i in range(100)]  # Array of x values
        y = [a * (i ** 2) + b * i + c for i in x]  # Array of corresponding y values
        plt.plot(x, y)

        plt.axhline(y=0, color="b", linestyle="--")
        plt.title(
            "".join(self._reduced_form),
        )
        # show the plot
        plt.savefig(graph_name + ".png")

    def _get_equation_parts(self):
        """
        This method use the type_listed_expression and dispatch it in two list respectively for the left part of the equation and the right part.
        """

        self._equation_left_part = []
        self._equation_right_part = []
        fill_left: bool = True
        equality_sign_found: bool = False
        question_sign_found: bool = False
        for elem in self._type_listed_expression:
            if question_sign_found is True:
                raise SyntaxError("Question sign should be the last character of an equation.")
            if isinstance(elem, Operator) and (
                elem.value == EQUALS_SIGN or elem.value == QUESTIONS_SIGN
            ):
                if elem.value == EQUALS_SIGN:
                    if equality_sign_found is True:
                        raise SyntaxError("More than one equality sign in the equation.")
                    else:
                        equality_sign_found = True
                        fill_left = False
                elif elem.value == QUESTIONS_SIGN:
                    if equality_sign_found is False:
                        raise SyntaxError(
                            "Question sign before any equality sign. Wrong equation format."
                        )
                    else:
                        question_sign_found = True
            elif fill_left is True:
                self._equation_left_part.append(elem)
            else:
                self._equation_right_part.append(elem)

    def _check_var_exponent(self, type_listed_expression):
        """
        Check if a var exponent is a non natural or negative number.
        """
        last_was_exponent_sign: bool = False
        last_was_var: bool = False
        for elem in type_listed_expression:

            if not isinstance(elem, Real) and last_was_exponent_sign and last_was_var:
                raise NotImplementedError(
                    f"Some part of the polynomial var have negative or non natural exponent."
                )
            elif isinstance(elem, Operator) and elem.value == EXPONENT_SIGN:
                last_was_exponent_sign = True
            elif isinstance(elem, Variable):
                last_was_var = True
            else:
                last_was_exponent_sign = False
                last_was_var = False

    def _check_vars(self):
        """
        Checking if there is one var and getting the name of it. Set to None otherwise.
        Also checking notImplemented operations.
        """
        self._var_name: str = ""
        for elem in self._equation_left_part + self._equation_right_part:
            if isinstance(elem, Variable):
                if self._var_name and elem.name != self._var_name:
                    raise SyntaxError(
                        "EquationSolver cannot handle more than one var for the moment."
                    )
                else:
                    self._var_name = elem.name

    def solve(
        self,
        type_listed_expression: list,
        verbose: bool = False,
        force_calculator_verbose: bool = False,
    ):
        self._verbose = verbose
        self._force_calculator_verbose = force_calculator_verbose
        self._type_listed_expression = type_listed_expression
        print("\nEQUATION SOLVER\n") if self._verbose is True else None

        print(
            "\nResolving following type_listed_expression equation : ", self._type_listed_expression
        ) if self._verbose is True else None

        self._get_equation_parts()

        self._equation_left_part = self._calculator.solve(
            type_listed_expression=self._equation_left_part,
            verbose=self._force_calculator_verbose,
            reduce_form_allowed=True,
        )

        self._equation_right_part = self._calculator.solve(
            type_listed_expression=self._equation_right_part,
            verbose=self._force_calculator_verbose,
            reduce_form_allowed=True,
        )

        if not isinstance(self._equation_left_part, Unresolved):
            ret = Unresolved()
            ret.append(self._equation_left_part)
            self._equation_left_part = ret
        if not isinstance(self._equation_right_part, Unresolved):
            ret = Unresolved()
            ret.append(self._equation_right_part)
            self._equation_right_part = ret
        for elem in self._equation_left_part + self._equation_right_part:
            # Checking for empty functions.
            if isinstance(elem, Function) and not elem.value:
                raise ValueError("A function have unknow value.")
        print("Left part equation = ", self._equation_left_part) if self._verbose is True else None
        print(
            "Right part equation = ", self._equation_right_part
        ) if self._verbose is True else None

        self._check_vars()

        if self._var_name != "":
            self._check_var_exponent(type_listed_expression=self._equation_left_part)
            self._check_var_exponent(type_listed_expression=self._equation_right_part)

        self._polynom_dict_left = self._get_polynom_dict(str(self._equation_left_part))
        self._polynom_dict_right = self._get_polynom_dict(str(self._equation_right_part))

        print("Polynom_dict_left = ", self._polynom_dict_left)
        print("Polynom_dict_right = ", self._polynom_dict_right)

        self._push_right_to_left()

        print("Polynom_dict_left = ", self._polynom_dict_left) if self._verbose is True else None
        print("Polynom_dict_right = ", self._polynom_dict_right) if self._verbose is True else None

        # Below if is only for equation without var
        if self._var_name == "":
            print(
                "There is no var in the equation, considering there is an X^0(=1), checking if the statement is true"
            ) if self._verbose is True else None
            if str(self._equation_left_part) == str(self._equation_right_part):
                self.solution = "X can be any real number."
            else:
                self.solution = "The equation is False."
            self._reducing_form()
        else:
            self._reducing_form()
            self._check_polynom_degree()

            print("Polynomial degree: ", self._polynom_degree) if self._verbose is True else None

            if self._polynom_degree > 2:
                raise NotImplementedError(
                    f"The polynomial degree is strictly greater than 2, the resolver is not implemented yet."
                )
            elif self._polynom_degree == 2:
                self._solve_polynom_degree_two()
            else:
                self._solve_polynom_degree_one()

        # Check if need to output graph
        if self._output_graph is True:
            import uuid

            self._create_graph_file(
                "Polynomial_degree_" + str(int(self._polynom_degree)) + "_" + str(uuid.uuid4())[1:6]
            )

        print("\nEND OF EQUATION SOLVER\n----------\n") if self._verbose is True else None
        return self.solution
