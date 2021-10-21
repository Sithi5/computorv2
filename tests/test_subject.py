import pytest

from src.expression_resolver import ExpressionResolver
from src.assignment.assigned_file import clear_assigned_file, open_and_deserialize_assigned_list

resolver = ExpressionResolver()


def test_subject():
    try:
        clear_assigned_file()
        assigned_list = open_and_deserialize_assigned_list()
        assert len(assigned_list) == 0

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

        ret = resolver.solve("varA = 2*i+3")
        assert str(ret) == "3.0 + 2.0i"

    except Exception:
        clear_assigned_file()
        raise
    clear_assigned_file()
