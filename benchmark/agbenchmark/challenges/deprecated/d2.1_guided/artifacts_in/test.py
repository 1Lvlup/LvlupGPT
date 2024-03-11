# mypy: ignore-errors
from typing import List  # Importing List type from typing module

from sample_code import two_sum  # Importing two_sum function from sample_code module


def test_two_sum(nums: List, target: int, expected_result: List[int]) -> None:
    # Function to test the two_sum function with given nums, target, and expected_result
    # Parameters:
    #   nums (List[int]): List of integers to find the two numbers that add up to the target
    #   target (int): The sum of two numbers to be found in the nums list
    #   expected_result (List[int]): The expected indices of the two numbers in the nums list
    # Returns: None

    result = two_sum(nums, target)  # Calling two_sum function with nums and target
    print(result)  # Printing the result from the two_sum function

    assert (
        result == expected_result
    ), f"AssertionError: Expected the output to be {expected_result}"  # Asserting the result matches the expected_result


if __name__ == "__main__":
    # Main block to run the test cases

    # test the trivial case with the first two numbers
    nums = [2, 7, 11, 15]  # Defining nums list
    target = 9  # Defining target
    expected_result = [0, 1]  # Defining expected_result
    test_two_sum(nums, target, expected_result)  # Calling test_two_sum function with nums, target, and expected_result

    # test for ability to use zero and the same number twice
    nums = [2, 7, 0, 15, 12, 0]  # Defining nums list
    target = 0  # Defining target
    expected_result = [2, 5]  # Defining expected_result
    test_two_sum(nums, target, expected_result)  # Calling test
