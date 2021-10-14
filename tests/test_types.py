import pytest

from src.types.types import *


def test_types_creation():
    # Test no args

    with pytest.raises(TypeError) as e:
        Real()
    assert str(e.value) == "__init__() missing 1 required positional argument: 'value'"

    # Test real
    Real("150")
    with pytest.raises(SyntaxError) as e:
        Real("150i")
    assert (
        str(e.value) == "An error occured when trying to create Real object with the value : 150i"
    )
    with pytest.raises(SyntaxError) as e:
        Real("[35]")
    assert (
        str(e.value) == "An error occured when trying to create Real object with the value : [35]"
    )

    # Test complex

    Complex(real_value="10", imaginary_value="i")
    Complex(real_value="10", imaginary_value="i")
    Complex(real_value="10", imaginary_value="i")
    with pytest.raises(SyntaxError) as e:
        complex = Complex(real_value="3", imaginary_value="[35]")
    assert (
        str(e.value)
        == "An error occured when trying to create Complex object: An error occured when trying to create Imaginary object with the value : [35]"
    )
    with pytest.raises(SyntaxError) as e:
        complex = Complex(real_value="3.12309i", imaginary_value="35")
    assert (
        str(e.value)
        == "An error occured when trying to create Complex object: An error occured when trying to create Real object with the value : 3.12309i"
    )
    Complex(real_value="35", imaginary_value="35")

    # Test functions
    Function(name="FN", argument="X")
    Function(name="FN", argument="15.2")
    Function(name="TESTNIMP", argument="15.2")
    with pytest.raises(SyntaxError) as e:
        Function(name="TEST5NIMP", argument="15.2")
    assert (
        str(e.value)
        == "An error occured when trying to create Function object with the name : TEST5NIMP and the argument : 15.2"
    )

    # Test matrice

    # Empty matrice
    with pytest.raises(SyntaxError) as e:
        Matrice(value="[]")
    assert (
        str(e.value) == "An error occured when trying to create Matrice object with the value : []"
    )
    # Wrong value
    with pytest.raises(SyntaxError) as e:
        Matrice(value="10")
    assert (
        str(e.value) == "An error occured when trying to create Matrice object with the value : 10"
    )

    # Wrong column sep
    with pytest.raises(SyntaxError) as e:
        Matrice(value="[[0],[0]]")
    assert (
        str(e.value)
        == "An error occured when trying to create Matrice object with the value : [[0],[0]]"
    )
    Matrice(value="[[0];[0]]")

    # No line
    with pytest.raises(SyntaxError) as e:
        Matrice(value="[0]")
    assert (
        str(e.value) == "An error occured when trying to create Matrice object with the value : [0]"
    )
    Matrice(value="[[0]]")

    # Wrong number of line
    with pytest.raises(SyntaxError) as e:
        Matrice(value="[[0];[0];[0,2]]")
    assert (
        str(e.value)
        == "An error occured when trying to create Matrice object with the value : [[0];[0];[0,2]]"
    )
    Matrice(value="[[0];[0];[0]]")

    # Wrong line sep
    with pytest.raises(SyntaxError) as e:
        Matrice(value="[[0;5];[0;5]]")
    assert (
        str(e.value)
        == "An error occured when trying to create Matrice object with the value : [[0;5];[0;5]]"
    )
    Matrice(value="[[0,5];[0,5]]")
