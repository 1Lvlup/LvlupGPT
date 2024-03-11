from sample_code import multiply_int


def test_multiply_int(num: int, multiplier, expected_result: int) -> None:
    """
    This function tests the multiply_int function from the sample_code module.
    It takes in three parameters: num (the number to be multiplied),
    multiplier (the number to multiply num by), and expected_result (the
    expected outcome of the multiplication).
    """
    result = multiply_int(num, multiplier)
    print(result)
    
    # The following line asserts that the result of the multiplication is
    # equal to the expected_result. If the assertion fails, an AssertionError
    # will be raised with a custom error message.
    assert (
        result == expected_result
    ), f"AssertionError: Expected the output to be {expected_result}"


if __name__ == "__main__":
    """
    This block of code is the entry point for the script. It creates a trivial
    test that has 4 as the num, and 2 as the multiplier. It then calls the
    test_multiply_int function with these values, along with the expected
    result of the multiplication (which is 8).
    """
    num = 4  # the number to be multiplied
    multiplier = 2  # the number to multiply num by
    expected_result = 8  # the expected outcome of the multiplication
    test_multiply_int(num, multiplier, expected_result)
