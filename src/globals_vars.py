import os

TESTS_VERBOSE = False

ASSIGNMENT_DIR_PATH: str = os.path.abspath(os.path.join(__file__, "..", "assignment"))
ASSIGNMENT_FILE_NAME: str = "variables.ser"
ASSIGNMENT_FILE_PATH: str = os.path.join(ASSIGNMENT_DIR_PATH, ASSIGNMENT_FILE_NAME)

GRAPH_DIR_PATH: str = os.path.abspath(os.path.join(__file__, "..", "..", "graphs"))

EQUALS_SIGN = "="
DIVISION_SIGN = "/"
MODULO_SIGN = "%"
QUESTIONS_SIGN = "?"
ADDITION_SIGN = "+"
SUBSTRACTION_SIGN = "-"
EXPONENT_SIGN = "^"
MULTIPLICATION_SIGN = "*"
MATRIX_MULTIPLICATION_SIGN = "@"

DIVIDING_OPERATORS = DIVISION_SIGN + MODULO_SIGN
OPERATORS = EXPONENT_SIGN + MULTIPLICATION_SIGN + DIVIDING_OPERATORS
MATRIX_OPERATORS = OPERATORS + MATRIX_MULTIPLICATION_SIGN
SIGN = ADDITION_SIGN + SUBSTRACTION_SIGN

OPERATORS_MINIMAL_PRIORITY = 1
OPERATORS_MAXIMAL_PRIORITY = 100

OPERATORS_PRIORITY = {
    DIVISION_SIGN: 2,
    MULTIPLICATION_SIGN: 2,
    MATRIX_MULTIPLICATION_SIGN: 2,
    MODULO_SIGN: 2,
    EXPONENT_SIGN: 3,
    ADDITION_SIGN: OPERATORS_MINIMAL_PRIORITY,
    SUBSTRACTION_SIGN: OPERATORS_MINIMAL_PRIORITY,
}

COMMA = "."

OPENING_PARENTHESES = "("
CLOSING_PARENTHESES = ")"

MATRIX_OPEN_PARENTHESES = "["
MATRIX_CLOSING_PARENTHESES = "]"
MATRIX_ROW_SEPARATOR = ","
MATRIX_COLUMN_SEPARATOR = ";"
