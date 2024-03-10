from typing import List, Tuple

def three_sum(nums: List[int], target: int) -> List[Tuple[int, int, int]]:
    """
    Given an array `nums` of n integers and a target number, find three integers in the array
    such that the sum is closest to the target.
    """
    nums.sort()
    result = []
    for i in range(len(nums) - 2):
        if i > 0 and nums[i] == nums[i - 1]:
            continue
        left, right = i + 1, len(nums) - 1
        while left < right:
            current_sum = nums[i] + nums[left] + nums[right]
            if current_sum == target:
                return [(nums[i], nums[left], nums[right])]
            elif current_sum < target:
                left += 1
            else:
                right -= 1
    return result

def test_three_sum(nums: List[int], target: int, expected_result: List[Tuple[int, int, int]]) -> None:
    result = three_sum(nums, target)
    print(result)
    assert result == expected_result, f"Expected the output to be {expected_result}"

if __name__ == "__main__":
    # test the trivial case with the first three numbers
    nums = [2, 7, 11, 15]
    target = 20
    expected_result = [(0, 1, 2)]
    test_three_sum(nums, target, expected_result)

    # test for ability to use zero and the same number twice
    nums = [2, 7, 0, 15, 12, 0]
    target = 2
    expected_result = [(0, 2, 5)]
    test_three_sum(nums, target, expected_result)

    # test for first and last index usage and negative numbers
