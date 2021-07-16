# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    equation_solver.py                                 :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: mabouce <ma.sithis@gmail.com>              +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/12/01 20:27:27 by mabouce           #+#    #+#              #
#    Updated: 2021/07/16 14:06:07 by mabouce          ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import re

from globals_vars import (
    _SIGN,
)

from utils import (
    convert_to_tokens,
    convert_signed_number,
    parse_sign,
    get_var_multiplier,
    add_implicit_cross_operator_for_vars,
    split_expression_parts_from_tokens,
)

from math_functions import my_power, my_round


class _EquationSolver:
    _tokens: list = []
    _left_part: list = []
    _right_part: list = []

    def __init__(self, calculator, output_graph: bool = False):
        self._output_graph = output_graph
        self._calculator = calculator

    def _check_vars(self):
        """
        Actually checking there is one and only one var and getting the name of it.
        Also checking notImplemented operations.
        """
        vars_list = re.findall(pattern=r"[A-Z]+", string="".join(self._tokens))
        # Removing duplicate var
        vars_set = list(set(vars_list))
        if len(vars_set) > 1:
            raise SyntaxError("EquationSolver cannot handle more than one var for the moment.")
        self.var_name = "".join(vars_set)

    def _check_have_var(self, var) -> bool:
        if self.var_name in var:
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
            if simplified_part[index] in _SIGN and len(part) > 0:
                if self._check_have_var(part):
                    power = self._get_power(part)
                    if power == 1:
                        polynom_dict["b"] = "-" + part if sign == "-" else part
                    elif power == 2:
                        polynom_dict["a"] = "-" + part if sign == "-" else part
                    else:
                        polynom_dict[str(power)] = "-" + part if sign == "-" else part
                else:
                    polynom_dict["c"] = "-" + part if sign == "-" else part
                part = ""
            if simplified_part[index] in _SIGN:
                sign = simplified_part[index]
            else:
                part = part + simplified_part[index]
            index += 1
        if self._check_have_var(part):
            power = self._get_power(part)
            if power == 1:
                polynom_dict["b"] = "-" + part if sign == "-" else part
            elif power == 2:
                polynom_dict["a"] = "-" + part if sign == "-" else part
            else:
                polynom_dict[str(power)] = "-" + part if sign == "-" else part
        else:
            polynom_dict["c"] = "-" + part if sign == "-" else part
        return polynom_dict

    def _push_right_to_left(self):
        for key, right_value in self._polynom_dict_right.items():
            try:
                left_value = self._polynom_dict_left[key]
            except:
                left_value = 0.0
            tokens = convert_to_tokens(
                convert_signed_number(
                    parse_sign(
                        add_implicit_cross_operator_for_vars(list(self.var_name), str(left_value))
                        + "-"
                        + add_implicit_cross_operator_for_vars(
                            list(self.var_name), str(right_value)
                        )
                    ),
                    accept_var=True,
                )
            )
            self._polynom_dict_left[key] = self._calculator.solve(
                tokens=tokens, verbose=self._force_calculator_verbose
            )

    def _check_polynom_degree(self):
        polynom_max_degree = 0.0
        for key, value in self._polynom_dict_left.items():
            if key == "a":
                if self.var_name in value and polynom_max_degree < 2:
                    polynom_max_degree = float(2)
                else:
                    continue
            elif key == "b":
                if self.var_name in value and polynom_max_degree < 1:
                    polynom_max_degree = float(1)
                else:
                    continue
            elif key == "c":
                continue
            elif float(key) > 2 and self.var_name in value and polynom_max_degree < float(key):
                polynom_max_degree = float(key)
        self._polynom_degree = polynom_max_degree

    def _get_discriminant(self, a: float, b: float, c: float) -> float:
        return my_power(b, 2) - 4.0 * a * c

    def _solve_polynom_degree_two(self):
        try:
            a = get_var_multiplier(self._polynom_dict_left["a"], var_name=self.var_name)
        except:
            a = 0.0
        try:
            b = get_var_multiplier(self._polynom_dict_left["b"], var_name=self.var_name)
        except:
            b = 0.0
        try:
            c = float(self._polynom_dict_left["c"])
        except:
            c = 0.0

        print("a = ", a, " b = ", b, " c = ", c) if self._verbose is True else None

        discriminant = self._get_discriminant(a, b, c)
        if discriminant > 0:
            print("The discriminant is strictly positive.")
        elif discriminant == 0:
            print("The discriminant is exactly zero.")
        else:
            print("The discriminant is strictly negative.")
        print("discriminant = ", discriminant)
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
            print("There is two solutions in complex number.")
            self.solution = []
            discriminant = -discriminant
            solution_one = convert_signed_number(
                f"{-b} / (2 * {a}) + i * {my_sqrt(discriminant)} / (2 * {a})".replace(" ", "")
            )
            tokens = convert_to_tokens(
                convert_signed_number(parse_sign(solution_one), accept_var=True)
            )
            self.solution.append(
                self._calculator.solve(tokens=tokens, verbose=self._force_calculator_verbose)
            )

            solution_two = f"{-b} / (2 * {a}) - i * {my_sqrt(discriminant)} / (2 * {a})".replace(
                " ", ""
            )
            tokens = convert_to_tokens(
                convert_signed_number(parse_sign(solution_two), accept_var=True)
            )
            self.solution.append(
                self._calculator.solve(tokens=tokens, verbose=self._force_calculator_verbose)
            )

    def _solve_polynom_degree_one(self):
        try:
            b = get_var_multiplier(self._polynom_dict_left["b"], var_name=self.var_name)
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

    def _check_var_negative_power(self, string: str):
        split = string.split(self.var_name + "^")
        index = 1
        while index < len(split):
            if split[index].startswith("-"):
                raise NotImplementedError(f"Some part of the polynomial var have negative power.")
            index += 1

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

        print("Reduced form : ", self._reduced_form)

    def _create_graph_file(self, graph_name: str = "equation_graph"):
        import matplotlib.pyplot as plt  # type: ignore

        try:
            a = get_var_multiplier(self._polynom_dict_left["a"], var_name=self.var_name)
        except:
            a = 0.0
        try:
            b = get_var_multiplier(self._polynom_dict_left["b"], var_name=self.var_name)
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

    def solve(self, tokens: list, verbose: bool = False, force_calculator_verbose: bool = False):
        self._verbose = verbose
        self._force_calculator_verbose = force_calculator_verbose
        self._tokens = tokens
        self._check_vars()
        splits_parts = split_expression_parts_from_tokens(self._tokens)
        self._left_part = splits_parts[0]
        self._right_part = splits_parts[1]

        print("\nEQUATION SOLVER\n") if self._verbose is True else None
        print("Reducing left equation :") if self._verbose is True else None
        simplified_left = self._calculator.solve(
            tokens=self._left_part, verbose=self._force_calculator_verbose
        )
        print("Reduced left : ", simplified_left) if self._verbose is True else None
        # Bellow both if for simplified part prevent float convertion to scientific notation
        if self.var_name not in simplified_left:
            simplified_left = f"{float(simplified_left):.6f}"
        print("Reducing right equation :") if self._verbose is True else None
        simplified_right = self._calculator.solve(
            tokens=self._right_part, verbose=self._force_calculator_verbose
        )
        print("Reduced right : ", simplified_right) if self._verbose is True else None
        if self.var_name not in simplified_right:
            simplified_right = f"{float(simplified_right):.6f}"
        if self.var_name != "":
            self._check_var_negative_power(simplified_left)
            self._check_var_negative_power(simplified_right)
        self._polynom_dict_left = self._get_polynom_dict(simplified_left)
        self._polynom_dict_right = self._get_polynom_dict(simplified_right)
        self._push_right_to_left()

        # Below if is only for equation without var
        if self.var_name == "":
            print(
                "There is no var in the equation, considering there is an X^0(=1), checking if the statement is true"
            )
            if simplified_left == simplified_right:
                self.solution = "X can be any real number."
            else:
                self.solution = "The equation is False."
            self._reducing_form()
        else:
            self._reducing_form()
            self._check_polynom_degree()

            print("Polynomial degree: ", self._polynom_degree)

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
