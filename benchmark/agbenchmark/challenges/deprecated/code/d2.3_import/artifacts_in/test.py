from typing import List, Tuple

def two_sum(nums: List[int], target: int) -> Tuple[int, int]:
    # Implement the two_sum function here
    pass


from typing import List

import unittest

from solution import two_sum


def test_two_sum(nums: List[int], target: int, expected_result: Tuple[int, int]) -> None:
    result = two_sum(nums, target)
    print(result)
    message = f"Expected {expected_result}, but got {result}"
    assert result == expected_result, message


class TestTwoSum(unittest.TestCase):
    def test_trivial_case(self):
        nums = [2, 7, 11, 15]
        target = 9
        expected_result = (0, 1)
        test_two_sum(nums, target, expected_result)

    def test_zero_and_same_number(self):
        nums = [2, 7, 0, 15, 12, 0]
        target = 0
        expected_result = (2, 5)
        test_two_sum(nums, target, expected_result)

    def test_first_and_last_index_and_negative_numbers(self):
        nums = [-6, 7, 11, 4]
        target = -2
        expected_result = (0, 3)
        test_two_sum(nums
