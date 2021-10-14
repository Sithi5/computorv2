from src.expression_resolver import ExpressionResolver
from src.math_utils import my_round


def test_expression_parsing():
    resolver = ExpressionResolver(verbose=False)

    # Simple test
    ret = resolver.solve(expression="5 * 5^0")
    assert ret.value == "5.0"

    # Simple test exponential
    ret = resolver.solve(expression="5 * 5^10")
    assert ret.value == "48828125.0"

    # Simple test with priority
    ret = resolver.solve(expression="5 * 5 + 10")
    assert ret.value == "35.0"

    # Simple test with float
    ret = resolver.solve(expression="5.3 * 5.2 + 10.8")
    assert ret.value == "38.36"

    # Test with parenthesis
    ret = resolver.solve(expression="5 * (5 + 10)")
    assert ret.value == "75.0"

    # Test with multiple parenthesis
    ret = resolver.solve(expression="5 * (5 + (10 * 50 + 2))")
    assert ret.value == "2535.0"

    # Test with multiple useless parenthesis
    ret = resolver.solve(expression="((((5 * (5 + (10 * 50 + 2))))))")
    assert ret.value == "2535.0"

    # Hard test with multiple parenthesis
    ret = resolver.solve(
        expression="5 * (5 + (10 * 50 + 24.15) *    50 * 18 *(12 + 52)) * (18 - (5 + 2))"
    )
    assert ret.value == "1660507475.0"

    # Hard test with float
    ret = resolver.solve(expression="545875785748.34444444478 * 5.2542 + 10456.81212")
    assert my_round(float(ret.value), 2) == my_round(2868140563935.763, 2)

    # Implicit multiplication with open parenthesis
    ret = resolver.solve(expression="25(5 + 2)")
    assert ret.value == "175.0"

    # Implicit multiplication with closing parenthesis
    ret = resolver.solve(expression="(5 + 2)25")
    assert ret.value == "175.0"

    # Test different parenthesis
    ret = resolver.solve(expression="(5 + 2}25")
    assert ret.value == "175.0"

    # Test different parenthesis
    ret = resolver.solve(expression="{5 + 2}25")
    assert ret.value == "175.0"

    # Test different parenthesis
    ret = resolver.solve(expression="(5 + 2}25")
    assert ret.value == "175.0"

    # Test multiplying by a signed number
    ret = resolver.solve(expression="5 * -10 + 599")
    assert ret.value == "549.0"

    # Test multiplying by a signed number
    ret = resolver.solve(expression="5 * +10")
    assert ret.value == "50.0"

    # Test multiplying by a signed number in parenthesis
    ret = resolver.solve(expression="5 * (+10)")
    assert ret.value == "50.0"

    # Test multiplying by a signed number in parenthesis
    ret = resolver.solve(expression="(+10)10")
    assert ret.value == "100.0"

    # Test substract by a signed number in parenthesis
    ret = resolver.solve(expression="(-10)-10")
    assert ret.value == "-20.0"

    # Test substract by a signed number in parenthesis
    ret = resolver.solve(expression="(-10)(-10)")
    assert ret.value == "100.0"

    # Test multiplying by a signed float
    ret = resolver.solve(expression="5 * -10.35843958432134 + 599")
    assert my_round(float(ret.value), 2) == my_round(547.2078020783933, 2)

    # Test sign before first number
    ret = resolver.solve(expression="-42-2")
    assert ret.value == "-44.0"
