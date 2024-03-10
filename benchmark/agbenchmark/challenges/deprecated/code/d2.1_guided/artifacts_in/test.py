from typing import List, Tuple

from sample_code import two_sum

def test_two_sum(nums: List, target: int, expected_result: Tuple[int, int]) -> None:
    result = two_sum(nums, target)
    print(result)
    assert result == expected_result, f"AssertionError: Expected the output to be {expected_result}"

if __name__ == "__main__":
    test_cases = [
        ([2, 7, 11, 15], 9, (0, 1)),
        ([2, 7, 0, 15, 12, 0], 0, (2, 5)),
        ([-6, 7, 11, 4], -2, (0, 3)),
    ]
    for nums, target, expected_result in test_cases:
        test_two_sum(nums, target, expected_result)
