# mypy: ignore-errors
from typing import List, Optional


def three_sum(nums: List[int], target: int) -> Optional[List[int]]:
    """
    Given an array of integers nums and an integer target, return indices of the three numbers such that the sum equals target.

    Args:
        nums (List[int]): A list of integers.
        target (int): An integer.

    Returns:
        Optional[List[int]]: A list of three indices, or None if no such triplet is found.
    """
    if not nums:
        return None

    nums_indices = sorted((num, index) for index, num in enumerate(nums))
    for i in range(len(nums_indices) - 2):
        if i > 0 and nums_indices[i] == nums_indices[i - 1]:
            continue
        left, right = i + 1, len(nums_indices) - 1
        while left < right:
            current_sum = nums_indices[i][0] + nums_indices[left][0] + nums_indices[right][0]
            if current_sum < target:
                left += 1
            elif current_sum > target:
                right -= 1
            else:
                return [nums_indices[i][1], nums_indices[left][1], nums_indices[right][1]]

    return None
