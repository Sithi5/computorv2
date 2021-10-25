import pytest

from src.expression_resolver import ExpressionResolver
from src.assignment.assigned_file import clear_assigned_file, open_and_deserialize_assigned_list


def test_wrong_type_assignment():
    resolver = ExpressionResolver()
    with pytest.raises(SyntaxError) as e:
        resolver.solve("5=2")
    assert str(e.value) == "Problem with assignment : trying to assign to a wrong type : Real"
    with pytest.raises(SyntaxError) as e:
        resolver.solve("i=2")
    assert str(e.value) == "Problem with assignment : trying to assign to a wrong type : Complex"
    with pytest.raises(SyntaxError) as e:
        resolver.solve("[[5i]]=2")
    assert str(e.value) == "Problem with assignment : trying to assign to a wrong type : Matrix"
    with pytest.raises(SyntaxError) as e:
        resolver.solve("[[30];[15]] ** [[5,2]] = 5")
    assert (
        str(e.value)
        == "Problem with assignment : the type_listed_expression is not well formated for assignment."
    )


def test_simple_assignment():
    clear_assigned_file()
    resolver = ExpressionResolver()
    resolver.solve("x=2")
    assigned_list = open_and_deserialize_assigned_list()
    assert len(assigned_list) == 1
    assert assigned_list[0].name == "X"
    assert assigned_list[0].value.value == "2"
