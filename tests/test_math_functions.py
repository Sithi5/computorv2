import pytest

from src.math_utils import is_natural, my_power, my_sqrt, my_round, my_atan, my_cos


def test_my_power():
    assert my_power(number=0, power=1500) == 0
    assert my_power(number=0, power=-1500) == 0
    assert my_power(number=0, power=0) == 1
    assert my_power(number=500, power=0) == 1
    assert my_power(number=-500, power=0) == 1
    assert my_power(number=-4.54221, power=0) == 1
    assert my_power(number=4.54221, power=0) == 1
    assert my_power(number=5, power=5) == 3125
    assert my_power(number=5, power=1000000000) == float("infinity")
    assert my_power(number=5, power=-1000000000) == 0
    with pytest.raises(ValueError) as e:
        ret = my_power(number=5, power=0.0000000000000000001) == 0
    assert str(e.value) == "irrational numbers are not accepted as exponent."
    assert str(e.value) == "irrational numbers are not accepted as exponent."
    assert my_power(number=0.0000000000000000000000000000001, power=2) == 1.0000000000000003e-62
    assert my_power(number=999999999999999999999999999999999999999, power=2) == float("infinity")
    assert my_power(number=3, power=-3) == 0.037037037037037035


def test_my_sqrt():
    assert my_sqrt(number=4) == 2
    assert my_sqrt(number=16) == 4
    assert my_sqrt(number=16.545) == 4.067554547882548
    assert my_sqrt(number=0.5454575) == 0.7385509461100161
    assert my_sqrt(number=1758) == 41.92851058647326
    assert my_sqrt(number=99999999999999) == 9999999.99999995
    assert my_sqrt(number=99999999999999999) == 316227766.01683795
    assert my_sqrt(number=0.00000025) == 0.0005000000000000059
    assert my_sqrt(number=0.00000033) == 0.0005744562646538029


def test_my_atan():
    assert my_atan(X=4) == 1.3258178488805414
    assert my_atan(X=4432.32151) == 1.5705710192836126


def test_my_cos():
    # ggle -0.65364362086
    assert my_cos(X=4) == -0.6536436208636144
    # ggle 0.00442569798
    assert my_cos(X=11) == 0.004413230561530001
    # ggle -0.70580730537
    assert my_cos(X=4432) == -0.9982264158710565


def test_my_round():
    # Test round up
    assert my_round(10.025, 2) == 10.03

    # Test multiple round up
    assert my_round(19.9951, 2) == 20.00

    assert my_round(10, 2) == 10

    with pytest.raises(ValueError) as e:
        my_round(10, 200000000) == 10
    assert str(e.value) == "Precision should be between 0 and 20"

    assert my_round(10, 20) == 10
    assert my_round(10, 0) == 10

    assert my_round(10.01234567891011121314555555555, 20) == 10.01234567891011121314555555555
    assert my_round(10.01234567891011121314555555555, 18) == 10.01234567891011121314555555555

    assert my_round(10.025, 10) == 10.025
    assert my_round(10.025454555557885454242, 10) == 10.0254545556

    assert my_round(10.025, 20) == 10.025
    assert my_round(10.025454555557885454242, 20) == 10.025454555557885454242
    assert my_round(10.0254545555578854542424444447585876545645, 20) == 10.025454555557885454242

    assert my_round(0.00000000000000000000000009, 20) == 0
    assert my_round(1.11111115e2, 1) == 111.1

    # Big round
    assert my_round(99999999999999999999999999999999999999, 20) == 1e38
    assert my_round(1e10, 5) == 10000000000.0

    # small round
    assert my_round(1e-100000, 20) == 0

    # Negative round
    assert my_round(-1.045754345454242, 6) == -1.045754
    assert my_round(-0.47513146390886934, 6) == -0.475131


def test_is_natural():
    assert is_natural(n="1") == True
    assert is_natural(n="1.0") == True
    assert is_natural(n="1.0") == True
    assert is_natural(n="-1.0") == True
    assert is_natural(n="-1.02") == False
    assert is_natural(n="1.02") == False
    assert is_natural(n="(1.02 + 6i)") == False
    assert is_natural(n="(1 + 6i)") == False
