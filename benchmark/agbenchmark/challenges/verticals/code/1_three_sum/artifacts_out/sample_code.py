# mypy: ignore-errors
from typing import List, Optional

def three_sum(nums: List[int], target: int) -> Optional[List[int]]:
    """
    This function takes a list of integers `nums` and an integer `target` as input.
    The goal is to find three numbers in `nums` that sum up to `target`.
    If such a triplet is found, the function returns a list of their indices;
    otherwise, it returns `None`.

    :param nums: A list of integers. This cannot be an empty list, as that would result in an immediate return of `None`.
    :param target: An integer.

    :return: Optional[List[int]]: A list of three indices, or `None` if no such triplet is found.
            
    The function first checks if `nums` is empty. If so, it immediately returns `None`.

    Next, it creates a new list `nums_indices` that contains tuples of each number in `nums`
    along with its index. This list is then sorted based on the numbers, ensuring that the
    smallest numbers come first.

    The function then iterates through `nums_indices`, skipping over any duplicate numbers
    (since they cannot contribute to new triplets). For each number, it performs a two-pointer
    search: it sets `left` and `right` to the indices immediately after and before the current index,
    respectively. It then repeatedly adjusts `left` and `right` until it finds a triplet that sums up to `target`.

    If the function exhausts all possible triplets without finding a matching one, it returns `None`.
    """
    if not nums:  # If nums is empty, return None
        return None

    nums_indices = sorted((num, index) for index, num in enumerate(nums))
    for i in range(len(nums_indices) - 2):
        if i > 0 and nums_indices[i] == nums_indices[i - 1]:
            continue  # Skip duplicates

