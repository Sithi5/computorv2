from typing import Type
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

    Complex("i")
    Complex("150i")
    Complex("150.23423i")
    with pytest.raises(SyntaxError) as e:
        Complex("[35]")
    assert (
        str(e.value)
        == "An error occured when trying to create Complex object with the value : [35]"
    )
    with pytest.raises(SyntaxError) as e:
        Complex("35")
    assert (
        str(e.value) == "An error occured when trying to create Complex object with the value : 35"
    )

    # Test functions
    Function("FN(X)")
    Function("FN(15.2)")
    Function("TESTNIMP(15.2)")
    with pytest.raises(SyntaxError) as e:
        Function("TEST5NIMP(15.2)")
    assert (
        str(e.value) == "An error occured when trying to create Function object with the value : TEST5NIMP(15.2)"
    )