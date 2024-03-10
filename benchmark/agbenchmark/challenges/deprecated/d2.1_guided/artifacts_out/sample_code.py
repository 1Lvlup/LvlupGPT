from typing import List, Optional

def two_sum(nums: List[int], target: int) -> Optional[List[int]]:
    """
    Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.

    Args:
    nums (List[int]): List of integers
    target (int): Target integer

    Returns:
    Optional[List[int]]: List of two indices that add up to target, or None if no such pair exists
    """
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return None
