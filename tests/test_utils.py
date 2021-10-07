from src.utils import convert_expression_to_upper


def test_convert_expression_to_upper():
    assert convert_expression_to_upper("I") == "i"
    assert convert_expression_to_upper("i") == "i"
    assert convert_expression_to_upper("ia") == "IA"
    assert convert_expression_to_upper("x=5i+iata") == "X=5i+IATA"
    assert convert_expression_to_upper("xyi*u+i-i*i=5i+iata") == "XYI*U+i-i*i=5i+IATA"
