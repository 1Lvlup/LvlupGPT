from typing import List  # Importing List type from typing module

from sample_code import two_sum  # Importing two_sum function from sample_code module


def test_two_sum(nums: List, target: int, expected_result: List[int]) -> None:  # Function to test the two_sum function
    result = two_sum(nums, target)  # Calling the two_sum function with nums and target as arguments
    print(result)  # Printing the result from the two_sum function
    assert (
        result == expected_result
    ), f"AssertionError: Expected the output to be {expected_result}"  # Asserting that the result matches the expected_result

