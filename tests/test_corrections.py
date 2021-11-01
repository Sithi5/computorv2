import pytest

from src.expression_resolver import ExpressionResolver
from src.assignment.assigned_file import clear_assigned_file


def test_corrections():
    try:
        clear_assigned_file()
        resolver = ExpressionResolver()

        # Small error testing
        with pytest.raises(SyntaxError) as e:
            resolver.solve("x == 2")
        assert (
            str(e.value) == "Equality operator '=' shouln't be follow by another equality operator."
        )
        with pytest.raises(SyntaxError) as e:
            resolver.solve("x = 23edd23-+-+")
        assert str(e.value) == "Operators or sign must be followed by a value or a variable."

        with pytest.raises(SyntaxError) as e:
            resolver.solve("=2")
        assert str(e.value) == "Equality operator '=' shouln't be placed at the first position."

        with pytest.raises(SyntaxError) as e:
            resolver.solve("3=2")
        assert str(e.value) == "Problem with assignment : trying to assign to a wrong type : Real"

        with pytest.raises(ValueError) as e:
            resolver.solve("x=g")
        assert str(e.value) == '("Couln\'t resolve the variable : ", Variable(G = Not defined))'

        with pytest.raises(SyntaxError) as e:
            resolver.solve("f(x = 2")
        assert str(e.value) == "Problem with parenthesis."

        with pytest.raises(SyntaxError) as e:
            resolver.solve("x = [[4,2]")
        assert str(e.value) == "Problem with matrix parenthesis."

        ret = resolver.solve("x = --2")
        assert str(ret) == "2.0"

        clear_assigned_file()
        resolver = ExpressionResolver()

        ret = resolver.solve("f(x) = x * 2")
        assert str(ret) == "X*2.0"

        with pytest.raises(ValueError) as e:
            ret = resolver.solve("t = f(x)")
        assert str(e.value) == "One of the variable/function have an unknow value."

        with pytest.raises(SyntaxError) as e:
            ret = resolver.solve("i = 2")
        assert (
            str(e.value) == "Problem with assignment : trying to assign to a wrong type : Complex"
        )

        # Elementary testing
        ret = resolver.solve("x = 2")
        assert str(ret) == "2.0"
        ret = resolver.solve("x = ?")
        assert str(ret) == "2.0"

        ret = resolver.solve("y = 4i")
        assert str(ret) == "4.0i"
        ret = resolver.solve("y = ?")
        assert str(ret) == "4.0i"

        ret = resolver.solve("z = [[2,3];[3,5]]")
        assert str(ret) == "[[2.0 , 3.0] ; [3.0 , 5.0]]"
        ret = resolver.solve("z = ?")
        assert str(ret) == "[[2.0 , 3.0] ; [3.0 , 5.0]]"

        clear_assigned_file()
        resolver = ExpressionResolver()

        # space and tab test
        ret = resolver.solve("x       \t\t     =\t\t         2")
        assert str(ret) == "2.0"

        clear_assigned_file()
        resolver = ExpressionResolver()

        # Semi-advenced testing
        ret = resolver.solve("x = 2")
        assert str(ret) == "2.0"

        ret = resolver.solve("y =       x")
        assert str(ret) == "2.0"
        ret = resolver.solve("y =?")
        assert str(ret) == "2.0"

        ret = resolver.solve("x = ?")
        assert str(ret) == "2.0"
        ret = resolver.solve("x = 5")
        assert str(ret) == "5.0"
        ret = resolver.solve("x = ?")
        assert str(ret) == "5.0"

        ret = resolver.solve("A = [[2,3]]")
        assert str(ret) == "[[2.0 , 3.0]]"
        ret = resolver.solve("A = ?")
        assert str(ret) == "[[2.0 , 3.0]]"
        ret = resolver.solve("B = A")
        assert str(ret) == "[[2.0 , 3.0]]"
        ret = resolver.solve("B = ?")
        assert str(ret) == "[[2.0 , 3.0]]"

        clear_assigned_file()
        resolver = ExpressionResolver()

        # Advenced testing
        resolver.solve("x = 2")
        ret = resolver.solve("y = x * [[4,2]]")
        assert str(ret) == "[[8.0 , 4.0]]"
        ret = resolver.solve("f(z) = z * y")
        assert str(ret) == "Z*[[8.0 , 4.0]]"
        ret = resolver.solve("f(z) =?")
        assert str(ret) == "Z*[[8.0 , 4.0]]"
        ret = resolver.solve("f(2) = ?")
        assert str(ret) == "[[16.0 , 8.0]]"

        clear_assigned_file()
        resolver = ExpressionResolver()

        resolver.solve("x = 2")
        ret = resolver.solve("f(x) = x * 5")
        assert str(ret) == "10.0"

        # Calc part
        # Simple test valid
        ret = resolver.solve("2 + 2 = ?")
        assert str(ret) == "4.0"
        ret = resolver.solve("3 *4 = ?")
        assert str(ret) == "12.0"
        resolver.solve("x = 2")
        ret = resolver.solve("x + 2 = ?")
        assert str(ret) == "4.0"

        with pytest.raises(ValueError) as e:
            resolver.solve("2 / 0 = ?")
        assert (
            str(e.value) == "('The expression lead to a division by zero : ', '2.0', ' / ', '0.0')"
        )
        with pytest.raises(ValueError) as e:
            resolver.solve("2 % 0 = ?")
        assert str(e.value) == "('The expression lead to a modulo zero : ', '2.0', ' % ', '0.0')"
        ret = resolver.solve("1.5 + 1= ?")
        assert str(ret) == "2.5"

        # Semi-advenced test valid
        resolver.solve("x = 2 * i")
        ret = resolver.solve("x ^2 = ?")
        assert str(ret) == "-4.0"

        clear_assigned_file()
        resolver = ExpressionResolver()

        ret = resolver.solve("A = [[2,3];[3,4]]")
        assert str(ret) == "[[2.0 , 3.0] ; [3.0 , 4.0]]"
        ret = resolver.solve("B = [[1,0];[0,1]]")
        assert str(ret) == "[[1.0 , 0.0] ; [0.0 , 1.0]]"
        ret = resolver.solve("A ** B")
        assert str(ret) == "[[2.0 , 3.0] ; [3.0 , 4.0]]"
        ret = resolver.solve("f(x) = x + 2")
        assert str(ret) == "X+2.0"
        ret = resolver.solve("p = 4")
        assert str(ret) == "4.0"
        ret = resolver.solve("f(p) = ?")
        assert str(ret) == "6.0"

        clear_assigned_file()
        resolver = ExpressionResolver()

        # Advenced test valid
        ret = resolver.solve("4 - 3 - (2 * 3) ^2 * (2 -4) + 4 = ?")
        assert str(ret) == "77.0"

        ret = resolver.solve("f(x) = 2 *( x + 3 * (x - 4))")
        assert str(ret) == "((X-4.0)*3.0+X)*2.0"
        resolver.solve("p = 2")
        ret = resolver.solve("f(3) - f(p) + 2 = ?")
        assert str(ret) == "10.0"

        resolver.solve("f(x) = 2 * x * i")
        ret = resolver.solve("f(2) = ?")
        assert str(ret) == "4.0i"

    except Exception:
        clear_assigned_file()
        raise
    clear_assigned_file()
