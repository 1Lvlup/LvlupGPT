from typing import List, Optional

def two_sum(nums: List[int], target: int) -> Optional[List[int]]:
    """
    This function takes a list of integers `nums` and an integer `target` as input.
    Its goal is to find a pair of indices in `nums` that add up to the `target` value.

    If such a pair is found, the function returns a list containing these two indices.
    If no such pair exists, the function returns `None`.

    :param nums: List of integers
    :param target: Target integer
    :return: List of two indices that add up to target, or `None` if no such pair exists
    """
    # `seen` is a dictionary that stores the numbers in `nums` as keys and their indices as values
    seen = {}
    for i, num in enumerate(nums):
        # Calculate the complement of the current number (i.e., the number that would add up to the target)
        complement = target - num
        
        # Check if the complement is in the `seen` dictionary
        if complement in seen:
            # If the complement is found, return a list containing the complement's index and the current index
            return [seen[complement], i]
        
        # If the complement is not found, add the current number and its index to the `seen` dictionary
        seen[num] = i
    
    # If no pair is found, return `None`
    return None
