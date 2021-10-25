from src.expression_resolver import ExpressionResolver
from src.assignment.assigned_file import clear_assigned_file, open_and_deserialize_assigned_list


def test_subject():
    try:
        clear_assigned_file()
        resolver = ExpressionResolver()
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
        assert str(ret) == "X^5.0*2.0+X^2.0*4.0-5.0*X+4.0"

        ret = resolver.solve(" funB(y) =43 * y / (4 % 2 * y)")
        # assert str(ret) == "43.0*Y/(4.0%2.0*Y)"
        ret = resolver.solve("funC(z) = -2 * z - 5")
        assert str(ret) == "-2.0*Z-5.0"

        # Reassignment
        ret = resolver.solve("x = 2")
        assert str(ret) == "2.0"
        ret = resolver.solve("y = x")
        assert str(ret) == "2.0"
        ret = resolver.solve("y = 7")
        assert str(ret) == "7.0"
        ret = resolver.solve("y =  2 * i - 4")
        assert str(ret) == "-4.0 + 2.0i"

        clear_assigned_file()
        resolver = ExpressionResolver()

        # Assign calc to var
        ret = resolver.solve("varA = 2 + 4 *2 - 5 %4 + 2 * (4 + 5)")
        assert str(ret) == "27.0"
        ret = resolver.solve("varB = 2 * varA - 5 %4")
        assert str(ret) == "53.0"
        ret = resolver.solve("funA(x) = varA + varB * 4 - 1 / 2 + x")
        assert str(ret) == "238.5+X"
        ret = resolver.solve("varC = 2 * varA - varB")
        assert str(ret) == "1.0"
        ret = resolver.solve("varD = funA(varC)")
        assert str(ret) == "239.5"

        # CALC PART

        clear_assigned_file()
        resolver = ExpressionResolver()

        ret = resolver.solve("a = 2 *4+4")
        assert str(ret) == "12.0"

        ret = resolver.solve("a +2 = ?")
        assert str(ret) == "14.0"

        # Image calc

        ret = resolver.solve("funA(x) = 2 * 4 + x")
        assert str(ret) == "8.0+X"

        ret = resolver.solve("funB(x) = 4 - 5 + (x + 2)^2 -4")
        assert str(ret) == "(X+2.0)^2.0+-1.0-4.0"

        ret = resolver.solve("funC(x) = 4x + 5 - 2")
        assert str(ret) == "4.0*X+5.0-2.0"

        ret = resolver.solve("funA(2) + funB(4) = ?")
        assert str(ret) == "41.0"

        ret = resolver.solve("funC(3) = ?")
        assert str(ret) == "15.0"

        # Quadratic equation

        ret = resolver.solve("funA(x) = x^2 + 2x + 1")
        assert str(ret) == "X^2.0+2.0*X+1.0"

        ret = resolver.solve("y=0")
        assert str(ret) == "0.0"

        ret = resolver.solve("funA(x) = y ?")
        assert str(ret) == "-1.0"

    except Exception:
        clear_assigned_file()
        raise
    clear_assigned_file()
