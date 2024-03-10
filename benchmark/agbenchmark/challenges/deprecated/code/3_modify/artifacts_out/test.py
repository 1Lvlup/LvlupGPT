from sample_code import multiply_int

def test_multiply_int():
    test_cases = [
        (4, 2, 8),
        (7, 7, 49),
        (-6, 2, -12),
        (0, 5, 0),
        (1, -3, -3),
    ]

    for num, multiplier, expected_result in test_cases:
        result = multiply_int(num, multiplier)
        print(f"{num} * {multiplier} = {result}")
        assert result == expected_result, f"AssertionError: Expected {expected_result} but got {result}"

if __name__ == "__main__":
    test_multiply_int()
