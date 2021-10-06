import argparse
import tkinter as tk
import logging


from src.expression_resolver import ExpressionResolver
from gui.app import Application
from src.assignment.assigned_file import clear_assigned_file, list_assigned_file


def resolve_input(resolver: ExpressionResolver, expression: str, debug: bool = False):
    if debug is False:
        try:
            result = resolver.solve(expression)
            if isinstance(result, list):
                print("The ", len(result), " solutions are :")
                for res in result:
                    print(res)
            else:
                print("result = ", result)
        except SyntaxError as e:
            logging.error("The expression syntax is not accepted : ")
            logging.error(e)
        except ValueError as e:
            logging.error("One of the value in the expression is not accepted : ")
            logging.error(e)
        except NotImplementedError as e:
            logging.error("One of the methods needed is not implemented yet : ")
            logging.error(e)
        except Exception as e:
            logging.critical("An exception appened : ")
            logging.error(e)
    else:
        logging.basicConfig(level=logging.DEBUG)
        result = resolver.solve(expression)
        if isinstance(result, list):
            print("The ", len(result), " solutions are :")
            for res in result:
                print(res)
        else:
            print("result = ", result)


def main_gui(resolver: ExpressionResolver):
    root = tk.Tk()
    app = Application(master=root, resolver=resolver)
    app.mainloop()


def print_shell_help():
    print(
        """
    Available commands:

    - help : Get available commands
    - list : List all saved variables
    - clear : Clear saved variables/matrices/functions
    - exit/quit/q : Quit program
    - v/verbose : Add/remove verbose
    - vv/vverbose : Add/remove full verbose
    - d/debug : Remove exception catching


    Resolve an expression:

    'expression'


    Assign a variable:

    'VariableName' '=' 'expression'


    Assign a function:

    'FunctionName(VariableName)' '=' 'expression'


    Assign a matrice:

    'MatriceName' '=' 'expression'


    Resolve a variable:

    'VariableName' '=' '?'


    Resolve a function:

    'FunctionName(Value)' '=' '?'


    """
    )


def shell_expression_resolver(resolver: ExpressionResolver):
    print_shell_help()
    debug = False
    while 1:
        expression = input("> ")
        if (
            expression.upper() == "EXIT"
            or expression.upper() == "QUIT"
            or expression.upper() == "Q"
        ):
            print("Exit ", __file__[0:-3], " shell.")
            break
        elif expression.upper() == "HELP":
            print_shell_help()
        elif expression.upper() == "CLEAR":
            clear_assigned_file()
            print("All assigned var have been cleared.")
        elif expression.upper() == "LIST":
            list_assigned_file()
        elif expression.upper() == "V" or expression.upper() == "VERBOSE":
            resolver.verbose = True if resolver.verbose is False else False
            resolver.force_calculator_verbose = False
            print("Verbose option : ", resolver.verbose)
            print("force_calculator_verbose option : ", resolver.force_calculator_verbose)
        elif expression.upper() == "VV" or expression.upper() == "VVERBOSE":
            if resolver.verbose is False or resolver.force_calculator_verbose is False:
                resolver.verbose = True
                resolver.force_calculator_verbose = True
            else:
                resolver.verbose = False
                resolver.force_calculator_verbose = False

            print("Verbose option : ", resolver.verbose)
            print("force_calculator_verbose option : ", resolver.force_calculator_verbose)
        elif expression.upper() == "D" or expression.upper() == "DEBUG":
            debug = True if debug is False else False
            print("Debug option : ", debug)
        else:
            resolve_input(resolver=resolver, expression=expression, debug=debug)


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
        "-d",
        "--debug",
        help="Remove exception catching.",
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
    logging.basicConfig(level=logging.DEBUG) if args.debug is True else None
    if args.gui:
        logging.debug("Launch in GUI mode.")
        main_gui(resolver=resolver)
    elif str(args.expression).lower() == "shell":
        logging.debug("""Starting inline shell expression resolver : """)
        shell_expression_resolver(resolver=resolver)
    else:
        resolve_input(resolver=resolver, expression=args.expression, debug=args.debug)


if __name__ == "__main__":
    main()
