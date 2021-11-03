import pytest

from src.globals_vars import TESTS_VERBOSE
from src.expression_resolver import ExpressionResolver

from src.assignment.assigned_file import clear_assigned_file


def test_calculator_quadratic_equation():
    try:
        clear_assigned_file()
        resolver = ExpressionResolver(verbose=TESTS_VERBOSE)

        ret = resolver.solve(expression="f(x) = -x ^ 2 +2x-3")
        assert str(ret) == "-X^2.0+2.0X-3.0"
        ret = resolver.solve(expression="f(x) = 0 ?")
        assert str(ret) == "['1.0 - 1.414214i', '1.0 + 1.414214i']"

        ret = resolver.solve(expression="f(x) = 5X^2 + 6x + 1")
        assert str(ret) == "5.0X^2.0+6.0X+1.0"
        ret = resolver.solve(expression="f(x) = 0 ?")
        assert str(ret) == "['-0.2', '-1.0']"

    except Exception:
        clear_assigned_file()
        raise
    clear_assigned_file()


def test_equation_computorv1_subject():
    try:

        clear_assigned_file()
        resolver = ExpressionResolver(verbose=TESTS_VERBOSE)

        resolver.solve(expression="f(x) = 5 * X^0 + 4 * X^1 - 9.3 * X^2")
        ret = resolver.solve(expression="f(x)= 1 * X^0 ?")
        assert str(ret) == "['-0.475131', '0.905239']"

        resolver.solve(expression="f(x) = 5 * X^0 + 4 * X^1 ")
        ret = resolver.solve(expression="f(x)= 4 * X^0 ?")
        assert str(ret) == "-0.25"
        with pytest.raises(NotImplementedError) as e:
            resolver.solve(expression="f(x) = 8 * X^0 - 6 * X^1 + 0 * X^2 - 5.6 * X^3 - 3 * X^0")
            resolver.solve(expression="f(x) =  3 * X^0 ? ")
        assert (
            str(e.value)
            == "The polynomial degree is strictly greater than 2, the resolver is not implemented yet."
        )

    except Exception:
        clear_assigned_file()
        raise
    clear_assigned_file()


def test_equation_degree_one():
    resolver = ExpressionResolver(verbose=False)

    resolver.solve(expression="f(x) = 5 * X^0 + 4 * X^1")
    ret = resolver.solve(expression="f(x)= 41 * X^0 ?")
    assert str(ret) == "9.0"

    resolver.solve(expression="f(x) = -51516544 * X^0 + 4241.1 * X^1 + 1213545")
    ret = resolver.solve(expression="f(x)= ---41 * X^0 + -X^1?")
    assert str(ret) == "11858.032106739585"

    resolver.solve(expression="f(x) = X ^1")
    ret = resolver.solve(expression="f(x) = X ^ 1?")
    assert str(ret) == "X can be any real number."

    resolver.solve(expression="f(x)=X")
    ret = resolver.solve(expression="f(x)=X?")
    assert str(ret) == "X can be any real number."

    resolver.solve(expression="f(x)=X^0")
    ret = resolver.solve(expression="f(x)=X^0?")
    assert str(ret) == "X can be any real number."

    resolver.solve(expression="f(x)=-0x^2 - -X^1  -0X^0")
    ret = resolver.solve(expression="f(x)=0?")
    assert str(ret) == "0.0"
    resolver.solve(expression="y = 0")
    ret = resolver.solve(expression="f(x)=y?")
    assert str(ret) == "0.0"

    # Multiplier small after var
    resolver.solve(expression="f(x)=X*0.001")
    ret = resolver.solve(expression="f(x)=0.000001?")
    assert str(ret) == "0.001"

    resolver.solve(expression="f(x)=X*0.001")
    ret = resolver.solve(expression="f(x)=-0.000001?")
    assert str(ret) == "-0.001"

    resolver.solve(expression="f(x)=5 * X^0 ")
    ret = resolver.solve(expression="f(x)= 4 * X^0 + 7 * X^1?")
    assert str(ret) == "0.14285714285714285"


def test_equation_degree_two():
    resolver = ExpressionResolver(verbose=False)

    resolver.solve(expression="f(x)=x^2+x-2 ")
    ret = resolver.solve(expression="f(x)= 0?")
    assert ret == ["1.0", "-2.0"]

    resolver.solve(expression="f(x)=x^2+3x+2")
    ret = resolver.solve(expression="f(x)= 0?")
    assert ret == ["-1.0", "-2.0"]

    resolver.solve(expression="f(x)=x ^2 + x + 1")
    ret = resolver.solve(expression="f(x)= 0?")
    assert ret == ["-0.5 + 0.866026i", "-0.5 - 0.866026i"]

    resolver.solve(expression="f(x)=4x ^2 + 4x + 1")
    ret = resolver.solve(expression="f(x)= 0?")
    assert ret == "-0.5"

    resolver.solve(expression="f(x)=-x ^2 + 2x - 3")
    ret = resolver.solve(expression="f(x)= 0?")
    assert ret == ["1.0 - 1.414214i", "1.0 + 1.414214i"]

    resolver.solve(expression="f(x)=x ^2 + 4x")
    ret = resolver.solve(expression="f(x)= 0?")
    assert ret == ["0.0", "-4.0"]

    resolver.solve(expression="f(x)=x ^2 -2x + 1")
    ret = resolver.solve(expression="f(x)= 0?")
    assert ret == "1.0"

    resolver.solve(expression="f(x)=x ^ 2 + 1")
    ret = resolver.solve(expression="f(x)= 0?")
    assert ret == ["i", "-i"]

    resolver.solve(expression="f(x)=x^2 -4x + 4 -1")
    ret = resolver.solve(expression="f(x)= 0?")
    assert ret == ["3.0", "1.0"]

    resolver.solve(expression="f(x)=X ^ 2 + X ^1 + x ^2")
    ret = resolver.solve(expression="f(x)= 0?")
    assert ret == ["0.0", "-0.5"]

    resolver.solve(expression="f(x)=X ^ 2 + X ^1 - x ^2")
    ret = resolver.solve(expression="f(x)= 0?")
    assert ret == "0.0"

    resolver.solve(expression="f(x)=-X ^ 2 + X ^1 + x ^2")
    ret = resolver.solve(expression="f(x)= 0?")
    assert ret == "0.0"

    resolver.solve(expression="f(x)=-X ^ 2 + X ^1 - x ^2")
    ret = resolver.solve(expression="f(x)= 0?")
    assert ret == ["0.0", "0.5"]

    resolver.solve(expression="f(x)=X ^ 2 + X ^1 + x ^1 ")
    ret = resolver.solve(expression="f(x)= 0?")
    assert ret == ["0.0", "-2.0"]

    resolver.solve(expression="f(x)=X ^ 2 - X ^1 + x ^1")
    ret = resolver.solve(expression="f(x)= 0?")
    assert ret == "0.0"

    resolver.solve(expression="f(x)=X ^ 2 - X ^1 - x ^1 ")
    ret = resolver.solve(expression="f(x)= 0?")
    assert ret == ["2.0", "0.0"]

    # 0 coeff
    resolver.solve(expression="f(x)=0x^2  ")
    ret = resolver.solve(expression="f(x)= 0?")
    assert ret == "X can be any real number."

    resolver.solve(expression="f(x)=0x^2 * X^1 10X^0")
    ret = resolver.solve(expression="f(x)= 0?")
    assert ret == "X can be any real number."

    resolver.solve(expression="f(x)=0x^2 * X^1  + 10X^0   ")
    ret = resolver.solve(expression="f(x)= 0?")
    assert ret == "The equation is False."

    resolver.solve(expression="f(x)=0x^2 + X^1  + 10X^0     ")
    ret = resolver.solve(expression="f(x)= 0?")
    assert ret == "-10.0"

    resolver.solve(expression="f(x)=-0x^2 + X^1  + 10X^0   ")
    ret = resolver.solve(expression="f(x)= 0?")
    assert ret == "-10.0"

    resolver.solve(expression="f(x)=-0x^2 - X^1  + 10X^0  ")
    ret = resolver.solve(expression="f(x)= 0?")
    assert ret == "10.0"

    resolver.solve(expression="f(x)=-x^2 - 0X^1  + 10X^0 ")
    ret = resolver.solve(expression="f(x)= 0?")
    assert ret == ["-3.162278", "3.162278"]

    resolver.solve(expression="f(x)=-x^2 - -0X^1  + 10X^0    ")
    ret = resolver.solve(expression="f(x)= 0?")
    assert ret == ["-3.162278", "3.162278"]

    resolver.solve(expression="f(x)=-x^2 - -0X^1  -0X^0    ")
    ret = resolver.solve(expression="f(x)= 0?")
    assert ret == "0.0"

    resolver.solve(expression="f(x)=-0x^2 - -0X^1  -0X^0   ")
    ret = resolver.solve(expression="f(x)= 0?")
    assert ret == "X can be any real number."

    # positive discriminant
    resolver.solve(expression="f(x)=5 * X^0 + 13 * X^1 + 3 * X^2")
    ret = resolver.solve(expression="f(x)= 1 * X^0 + 1 * X^1?")
    assert ret == ["-0.367007", "-3.632993"]

    # Zero discriminant
    resolver.solve(expression="f(x)=6 * X^0 + 11 * X^1 + 5 * X^2")
    ret = resolver.solve(expression="f(x)= 1 * X^0 + 1 * X^1?")
    assert ret == "-1.0"

    # Negative discriminant
    resolver.solve(expression="f(x)=5 * X^0 + 3 * X^1 + 3 * X^2")
    ret = resolver.solve(expression="f(x)=  1 * X^0 + 0 * X^1?")
    assert ret == ["-0.5 + 1.040833i", "-0.5 - 1.040833i"]


def test_equations_infinite_solution():
    resolver = ExpressionResolver(verbose=False)

    # Numbers only
    resolver.solve(expression="f(x)=2")
    ret = resolver.solve(expression="f(x)=  2?")
    assert ret == "X can be any real number."

    resolver.solve(expression="f(x)=5 * X^0")
    ret = resolver.solve(expression="f(x)=  5 * X^0?")
    assert ret == "X can be any real number."

    resolver.solve(expression="f(x)=4 * X^0")
    ret = resolver.solve(expression="f(x)= 8?")
    assert ret == "The equation is False."

    # Float only
    resolver.solve(expression="f(x)=2.2456")
    ret = resolver.solve(expression="f(x)= 2.2456?")
    assert ret == "X can be any real number."


def test_wrong_equation():
    resolver = ExpressionResolver(verbose=False)

    # Numbers only false
    resolver.solve(expression="f(x)=2")
    ret = resolver.solve(expression="f(x)= -2?")
    assert ret == "The equation is False."

    # Numbers with var^0 false
    resolver.solve(expression="f(x)=2*X^0")
    ret = resolver.solve(expression="f(x)= -2*X^0?")
    assert ret == "The equation is False."

    # Float only false
    resolver.solve(expression="f(x)=2.2456")
    ret = resolver.solve(expression="f(x)=  -2.2456?")
    assert ret == "The equation is False."

    # power var with negative value
    with pytest.raises(NotImplementedError) as e:
        resolver.solve(expression="f(x)=2")
        ret = resolver.solve(expression="f(x)=  -2X^-5?")
    assert str(e.value) == "Some part of the polynomial var have negative power."

    # # power var with negative value
    with pytest.raises(NotImplementedError) as e:
        resolver.solve(expression="f(x)=2")
        ret = resolver.solve(expression="f(x)=  -2X^(-5)?")
    assert str(e.value) == "Some part of the polynomial var have negative power."

    # # power var with irrational value
    with pytest.raises(NotImplementedError) as e:
        resolver.solve(expression="f(x)=2")
        ret = resolver.solve(expression="f(x)=  -2X^5.00000005?")
    assert (
        str(e.value)
        == "The polynomial degree is strictly greater than 2, the resolver is not implemented yet."
    )

    # power var with negative irrational value
    with pytest.raises(NotImplementedError) as e:
        resolver.solve(expression="f(x)=2")
        ret = resolver.solve(expression="f(x)=  -2X^-5.00000005?")
    assert str(e.value) == "Some part of the polynomial var have negative power."

    # power var with negative non natural value
    with pytest.raises(NotImplementedError) as e:
        resolver.solve(expression="f(x)=2")
        ret = resolver.solve(expression="f(x)= -2X^((-5.00000005))?")
    assert str(e.value) == "Some part of the polynomial var have negative power."

    with pytest.raises(NotImplementedError) as e:
        resolver.solve(expression="f(x)=x^3 + 2x^2 -3x")
        ret = resolver.solve(expression="f(x)= 0?")
    assert (
        str(e.value)
        == "The polynomial degree is strictly greater than 2, the resolver is not implemented yet."
    )

    # # Nothing left
    with pytest.raises(SyntaxError) as e:
        resolver.solve(expression="f(x)=")
        ret = resolver.solve(expression="f(x)= 0?")
    assert (
        str(e.value)
        == "Problem with assignment : the type_listed_expression is not well formated for assignment."
    )


def test_others():
    resolver = ExpressionResolver(verbose=False)

    resolver.solve(expression="f(x)=0 ")
    ret = resolver.solve(expression="f(x)= X + X?")
    assert ret == "0.0"

    resolver.solve(expression="f(x)=0 ")
    ret = resolver.solve(expression="f(x)= X ^ 2 + X^ 2?")
    assert ret == "0.0"
