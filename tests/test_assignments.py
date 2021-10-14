import pytest

from src.expression_resolver import ExpressionResolver
from src.assignment.assigned_file import clear_assigned_file, open_and_deserialize_assigned_list

resolver = ExpressionResolver()


# def test_wrong_type_assignment():
#     with pytest.raises(SyntaxError) as e:
#         resolver.solve("5=2")
#     assert str(e.value) == "Problem with assignment : trying to assign to a wrong type : Real"
#     with pytest.raises(SyntaxError) as e:
#         resolver.solve("5i=2")
#     assert str(e.value) == "Problem with assignment : trying to assign to a wrong type : Complex"
#     with pytest.raises(SyntaxError) as e:
#         resolver.solve("[5i]=2")
#     assert str(e.value) == "Problem with assignment : trying to assign to a wrong type : Matrice"


# def test_simple_assignment():
#     clear_assigned_file()
#     resolver.solve("x=2")
#     assigned_list = open_and_deserialize_assigned_list()
#     assert len(assigned_list) == 1
#     assert assigned_list[0].name == "X"
