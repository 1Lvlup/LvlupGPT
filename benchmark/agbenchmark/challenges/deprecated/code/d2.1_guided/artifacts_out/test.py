from typing import List, Tuple

from sample_code import two_sum  # Import the two_sum function from sample_code module

def test_two_sum(nums: List, target: int, expected_result: Tuple[int, int]) -> None:
    """
    Test the two_sum function with given nums and target,
    and compare the result with the expected_result.

    :param nums: List[int] - A list of integers
    :param target: int - The target integer to find the pair of indices for
    :param expected_result: Tuple[int, int] - The expected pair of indices
    :return: None
    """
    result = two_sum(nums, target)  # Call the two_sum function with nums and target
    print(result)  # Print the result for debugging or visualization purposes
    assert result == expected_result, f"AssertionError: Expected the output to be {expected_result}"  # Assert that the result matches the expected_result

if __name__ == "__main__":
    test_cases = [
        ([2, 7, 11, 15], 9, (0, 1)),
        ([2, 7, 0, 15, 12, 0], 0, (2, 5)),
        ([-6, 7, 11, 4], -2, (0, 3)),
    ]

    """
    Iterate through the test_cases, calling the test_two_sum function for each case.
    This allows for automated testing of the two_sum function with different inputs and expected outputs.
    """
    for nums, target, expected_result in test_cases:
        test_two_sum(nums, target, expected_result)
