from typing import List, Optional

def three_sum(nums: List[int], target: int) -> Optional[List[int]]:
    # Create a list of tuples, where each tuple contains a number and its index in the original nums list
    nums_indices = [(num, index) for index, num in enumerate(nums)]
    
    # Sort the nums_indices list based on the numbers
    nums_indices.sort()
    
    # Iterate through the sorted nums_indices list with an index 'i'
    for i in range(len(nums_indices) - 2):
        # Skip the current iteration if the current and previous numbers are the same
        if i > 0 and nums_indices[i] == nums_indices[i - 1]:
            continue
        
        # Initialize 'l' and 'r' as the index after 'i' and the last index of nums_indices respectively
        l, r = i + 1, len(nums_indices) - 1
        
        # Continue the inner loop while 'l' is less than 'r'
        while l < r:
            # Calculate the sum of the three numbers at indices 'i', 'l', and 'r'
            three_sum = nums_indices[i][0] + nums_indices[l][0] + nums_indices[r][0]
            
            # If the sum is less than the target, increment 'l'
            if three_sum < target:
                l += 1
            # If the sum is greater than the target, decrement 'r'
            elif three_sum > target:
                r -= 1
            # If the sum is equal to the target, return a sorted list of the indices
            else:
                indices = sorted(
                    [nums_indices[i][1], nums_indices[l][1], nums_indices[r][1]]
                )
                return indices
    
    # If no triplets with the target sum are found, return None
    return None
