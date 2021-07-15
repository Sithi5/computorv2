# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    computorv2.py                                      :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: mabouce <ma.sithis@gmail.com>              +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/12/01 20:27:45 by mabouce           #+#    #+#              #
#    Updated: 2021/07/15 19:19:13 by mabouce          ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import argparse
import tkinter as tk

from expression_resolver import ExpressionResolver
from GUI.app import Application
from utils_saving_variables import clear_variables_file


def resolve_input(resolver: ExpressionResolver, expression: str):
    # try:
    result = resolver.solve(expression)
    if isinstance(result, list):
        print("The ", len(result), " solutions are :")
        for res in result:
            print(res)
    else:
        print("result = ", result)


# except SyntaxError as e:
#     print("The expression syntax is not accepted : ", e)
# except ValueError as e:
#     print("One of the value in the expression is not accepted : ", e)
# except NotImplementedError as e:
#     print("One of the methods needed is not implemented yet : ", e)
# except NothingToDoError as e:
#     print(e)
# except Exception as e:
# print("An exception appened : ", e)


def main_gui(resolver: ExpressionResolver):
    root = tk.Tk()
    app = Application(master=root, resolver=resolver)
    app.mainloop()


def print_shell_help():
    print(
        """
    Available commands:

    - HELP : Get available commands
    - CLEAR : Clear saved variables/matrices/functions
    - EXIT : Quit program
    - QUIT : Quit program


    Resolve an expression:

    'expression'


    Assign a variable:

    'VariableName' '=' 'expression'


    Assign a function:

    'FunctionName(VariableName)' '=' 'expression'


    Assign a matrice:

    'MatriceName' '=' 'expression'


    Resolve a variable/matrice:

    'VariableName'/'MatriceName'/'FunctionName(VariableName)' '=' '?'


    Resolve a function:

    'FunctionName(Value)' '=' '?'


    """
    )


def shell_expression_resolver(resolver: ExpressionResolver):
    print_shell_help()
    while 1:
        expression = input("> ")
        if expression.upper() == "EXIT" or expression.upper() == "QUIT":
            print("Exit ", __file__[0:-3], " shell.")
            break
        elif expression.upper() == "HELP":
            print_shell_help()
        elif expression.upper() == "CLEAR":
            clear_variables_file()
            print("All variables have been cleared.")
        else:
            resolve_input(resolver=resolver, expression=expression)


def main(argv=None):
    print()
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--gui",
        help="Launch computor in GUI mode",
        action="store_true",
    )
    parser.add_argument(
        "-e",
        "--expression",
        help="Insert expression to resolve. Insert 'shell' if you want inline shell expression resolver.",
        default="shell",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        help="Add verbose and print different resolving step.",
        action="store_true",
    )
    parser.add_argument(
        "-vv",
        "--force_calculator_verbose",
        help="Add all verbose and force the calculator verbose.",
        action="store_true",
    )
    parser.add_argument(
        "--output_graph",
        help="In case there is a possible graph to create, it will output it in a new file.",
        action="store_true",
    )
    args = parser.parse_args(argv)

    resolver = ExpressionResolver(
        verbose=args.verbose | args.force_calculator_verbose,
        force_calculator_verbose=args.force_calculator_verbose,
        output_graph=args.output_graph,
    )
    if args.gui:
        print("Launch in GUI mode.")
        main_gui(resolver=resolver)
    elif str(args.expression).lower() == "shell":
        print("""Starting inline shell expression resolver : """)
        shell_expression_resolver(resolver=resolver)
    else:
        resolve_input(resolver=resolver, expression=args.expression)


if __name__ == "__main__":
    main()
