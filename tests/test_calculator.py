from src.expression_resolver import ExpressionResolver


def test_calculator_complex():
    resolver = ExpressionResolver(verbose=False)

    # Simple test
    ret = resolver.solve(expression="5 * 5i")
    assert str(ret) == "25.0i"

    # Add complex
    ret = resolver.solve(expression="(123847.2193812 - 5i) + 2i")
    assert str(ret) == "123847.219381 - 3.0i"
    ret = resolver.solve(expression="(99 - 5i) - (1 +2i)")
    assert str(ret) == "98.0 - 7.0i"

    # Dividing complex
    ret = resolver.solve(expression="(5i) / 2")
    assert str(ret) == "2.5i"
    ret = resolver.solve(expression="(5i) / (5 + 255i)")
    assert str(ret) == "0.0196 + 0.000384i"

    # Mod complex
    ret = resolver.solve(expression="(5i) % 2")
    assert str(ret) == "i"
    ret = resolver.solve(expression="(123+ 5i) % 54")
    assert str(ret) == "15.0 + 5.0i"

    # Power complex
    ret = resolver.solve(expression="(5i) ^ 2")
    assert str(ret) == "-25.0"
    ret = resolver.solve(expression="(5i) ^ 0")
    assert str(ret) == "1.0"
    ret = resolver.solve(expression="(5 + 5i) ^ 2")
    assert str(ret) == "50.0i"


def test_calculator_matrice():
    resolver = ExpressionResolver(verbose=False)

    pass
