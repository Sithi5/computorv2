import pytest

from src.expression_resolver import ExpressionResolver
from src.assignment.assigned_file import clear_assigned_file, open_and_deserialize_assigned_list

resolver = ExpressionResolver()


def test_subject():
    try:
        clear_assigned_file()
        assigned_list = open_and_deserialize_assigned_list()
        assert len(assigned_list) == 0

        # R
        resolver.solve("varA = 2")
        assigned_list = open_and_deserialize_assigned_list()
        assert len(assigned_list) == 1
        assert assigned_list[0].name == "varA".upper()
        assert assigned_list[0].value.value == "2"

        resolver.solve("varB = 4.242")
        assigned_list = open_and_deserialize_assigned_list()
        assert len(assigned_list) == 2
        assert assigned_list[0].name == "varA".upper()
        assert assigned_list[0].value.value == "2"
        assert assigned_list[1].name == "varB".upper()
        assert assigned_list[1].value.value == "4.242"

        ret = resolver.solve("varB = 4.242")
        assert str(ret) == "4.242"

        ret = resolver.solve("varC = -4.3")
        assert str(ret) == "-4.3"

        # Complex

        ret = resolver.solve("varA = 2*i+3")
        assert str(ret) == "3.0 + 2.0i"

        ret = resolver.solve("varB = -4i-4")
        assert str(ret) == "-4.0 - 4.0i"

        # Matrix

        ret = resolver.solve("varA = [[2,3];[4,3]]")
        assert str(ret) == "[[2.0 , 3.0] ; [4.0 , 3.0]]"
        ret = resolver.solve("varB = [[3,4]]")
        assert str(ret) == "[[3.0 , 4.0]]"

        # Function

        ret = resolver.solve("funA(x) = 2*x^5 + 4x^2 - 5*x + 4")
        assert str(ret) == "2 * x^5 + 4 * x^2 - 5*x + 4"
        ret = resolver.solve("43 * y / (4 % 2 * y)")
        assert str(ret) == "[[3.0 , 4.0]]"
        ret = resolver.solve("funC(z) = -2 * z - 5")
        assert str(ret) == "-2 * z - 5"

        # Reassignment
        ret = resolver.solve("x = 2")
        assert str(ret) == "2.0"
        ret = resolver.solve("y = x")
        assert str(ret) == "2.0"
        ret = resolver.solve("y = 7")
        assert str(ret) == "7.0"
        ret = resolver.solve("y =  2 * i - 4")
        assert str(ret) == "-4.0 + 2.0i"

        # Assign calc to var
        ret = resolver.solve("varA = 2 + 4 *2 - 5 %4 + 2 * (4 + 5)")
        assert str(ret) == "27.0"
        ret = resolver.solve("varB = 2 * varA - 5 %4")
        assert str(ret) == "53.0"
        ret = resolver.solve("funA(x) = varA + varB * 4 - 1 / 2 + x")
        assert str(ret) == "238.5 + X"
        ret = resolver.solve("varC = 2 * varA - varB")
        assert str(ret) == "1.0"
        ret = resolver.solve("varD = funA(varC)")
        assert str(ret) == "239.5"

    except Exception:
        clear_assigned_file()
        raise
    clear_assigned_file()
