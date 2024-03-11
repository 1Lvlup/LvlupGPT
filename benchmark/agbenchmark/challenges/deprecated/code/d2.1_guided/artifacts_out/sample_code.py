from typing import List

def two_sum(nums: List[int], target: int) -> List[int]:
    """
    This function takes a list of integers `nums` and an integer `target` as input.
    The goal is to find two numbers in `nums` that add up to the `target` value.
    If such numbers are found, the function returns a list of their indices in the original `nums` list.

    Parameters:
    - nums (List[int]): a list of integers
    - target (int): an integer

    Returns:
    - List[int]: a list of two integers representing the indices of the two numbers in `nums` that add up to `target`

    Raises:
    - ValueError: if the input list has less than two elements
    """
    if len(nums) < 2:
        # The function requires at least two elements in the input list to find a pair of numbers that add up to the target.
        # If the list has less than two elements, a ValueError is raised.
        raise ValueError("Input list must have at least two elements")

    seen = {}  # A dictionary to store the numbers we've seen so far and their indices.
    for i, num in enumerate(nums):
        # Iterate through the input list and its elements.
        complement = target - num  # Calculate the complement of the current number.
        if complement in seen:
            # If the complement is in the dictionary, it means we've found a pair of numbers that add up to the target.
            return [seen[complement], i]  # Return their indices.
        seen[num] = i  # If the complement is not found, add the current number and its index to the dictionary.
