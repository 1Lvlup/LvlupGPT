# mypy: ignore-errors
from typing import List, NamedTuple, Union  # Importing List, NamedTuple, and Union from the typing module

from sample_code import three_sum  # Importing the three_sum function from the sample_code module

class TestCase(NamedTuple):
    # Defining a new named tuple class called TestCase, which will be used to represent a test case
    # for the three_sum function. It has two attributes: nums (a list of integers) and target (an integer).
    nums: List[int]
    target: int


test_cases: List[TestCase] = [    # Defining a list of test cases to use in testing the three_sum function.
    TestCase(nums=[-1, 0, 1, 2, -1, -4], target=0),
    TestCase(nums=[0, 1, 1], target=2),
    TestCase(nums=[-1, -1, 1, 1], target=0),
]

for test in test_cases:  # Iterating over each test case in the test_cases list.
    result: List[List[int]] = three_sum(test.nums, test.target)  # Calling the three_sum function with the current test case's nums and target attributes.
                                                                 # The result of the function call is stored in the result variable.
    print(f"Three sums of {test.target} for nums {test.nums}: {result}")  # Printing a message that includes the current test case's nums and target attributes,
                                                                         # as well as the result of calling the three_sum function.
