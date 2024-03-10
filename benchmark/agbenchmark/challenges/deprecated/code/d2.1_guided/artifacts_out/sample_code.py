from typing import List

def two_sum(nums: List[int], target: int) -> List[int]:
    """
    Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.

    Args:
    - nums: List[int] - a list of integers
    - target: int - an integer

    Returns:
    List[int] - a list of two integers [i, j] such that nums[i] + nums[j] == target

    Raises:
    ValueError: if the input list has less than two elements
    """
    if len(nums) < 2:
        raise ValueError("Input list must have at least two elements")

    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
