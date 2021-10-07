import logging


def my_power(number: float, power: int) -> float:
    if power != int(power):
        raise ValueError("irrational numbers are not accepted as exponent.")

    if power == 0:
        return 1.0
    elif number == 0:
        return 0.0

    # Checking for Nan
    if power != power:
        return power
    elif number != number:
        return number

    infinity_float = float("infinity")
    negative_infinity_float = float("-infinity")
    if power == negative_infinity_float or power == infinity_float:
        return power

    result = 1.0

    if power > 0:
        while power > 0:
            result *= number
            power -= 1
            if result > 99999999999999999999999999999999:
                result = float("Infinity")
            elif result < -99999999999999999999999999999999:
                result = float("-Infinity")
            if result == float("Infinity") or result == 0 or result == float("-Infinity"):
                return result
    elif power == 0:
        result = 1
    else:
        while power < 0.0:
            result /= number
            power += 1
            if result < 0.000000000000000000000000000001:
                result = 0
            if result == float("Infinity") or result == 0 or result == float("-Infinity"):
                return result
    return result


def my_abs(number: float) -> float:
    if number < 0:
        return number * -1
    return number


def my_sqrt(number: float):
    infinity_float = float("infinity")
    negative_infinity_float = float("-infinity")

    # Checking for Nan
    if number != number:
        return number

    if number == negative_infinity_float or number == infinity_float:
        return number

    if number < 0.0:
        raise ValueError("input should be a positive number.")

    result = number
    precision = my_power(10, -15)
    index = 0
    while my_abs(number - result * result) > precision:
        last_result = result
        result = (result + number / result) / 2
        if last_result == result:
            break
        index += 1
    return my_round(result, precision=20)


def my_round(number: float, precision: int = 6) -> float:
    """
    Round the number after 'precision' digits after the comma.
    """

    if number == float("-infinity") or number == float("infinity"):
        logging.debug("Couln't round infinity.")
        return number

    # Checking for Nan
    if number != number:
        return number
    if precision != precision:
        raise ValueError("Precision is Nan.")

    if precision > 20 or precision < 0:
        raise ValueError("Precision should be between 0 and 20")

    return float(format(number, f".{precision}f"))


def is_real(n: str) -> bool:
    try:
        float(n)
        return True
    except ValueError:
        return False


def my_atan(X: float):
    """
    Return the arc tangente in rad.
    """
    A: float = 1.0 / my_sqrt(1.0 + (X * X))
    B = 1.0
    N = 1
    while N <= 11:
        A = (A + B) / 2.0
        B = my_sqrt(A * B)
        N += 1
    return X / (my_sqrt(1.0 + (X * X)) * A)


def my_cos(X: float):
    """
    Return the approximate cosinus.
    """
    R = X * X
    S = 42.0
    N = 10
    while N >= 1:
        S = 4.0 * N - 2.0 + (-R) / S
        N -= 1
    S = S * S
    return (S - R) / (S + R)
