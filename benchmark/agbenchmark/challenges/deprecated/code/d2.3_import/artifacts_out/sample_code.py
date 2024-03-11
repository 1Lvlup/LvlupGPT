from typing import List, Optional

def two_sum(nums: List, target: int) -> Optional[List[int]]:
    # Initialize an empty dictionary to keep track of the numbers and their indices
    seen = {}

    # Iterate through the list of numbers
    for i, num in enumerate(nums):
        # Calculate the complement of the current number
        complement = target - num

        # Check if the complement is in the dictionary
        if complement in seen:
            # If it is, return a list of the indices of the complement and the current number
            return [seen[complement], i]

        # If the complement is not in the dictionary, add the current number and its index to the dictionary
        seen[num] = i

    # If the function goes through the entire list without finding two numbers that add up to the target, return None
    return None
