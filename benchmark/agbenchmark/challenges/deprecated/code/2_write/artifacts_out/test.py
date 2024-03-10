from sample_code import multiply_int

def test_multiply_int(num: int, expected_result: int) -> None:
    result = multiply_int(num)
    print(f"Result: {result}")
    assert result == expected_result, f"AssertionError: Expected the output to be {expected_result} but got {result}"

if __name__ == "__main__":
    # test the trivial case
    num = 4
    expected_result = 8
    test_multiply_int(num, expected_result)

    # test another case
    num = 0
    expected_result = 0
    test_multiply_int(num, expected_result)

    # test negative case
    num = -3
    expected_result = -6
    test_multiply_int(num, expected_result)
