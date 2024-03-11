from sample_code import multiply_int  # Import the multiply_int function from the sample_code module

def test_multiply_int(num: int, multiplier, expected_result: int) -> None:   # Define a function to test the multiply_int function
    result = multiply_int(num, multiplier)  # Call the multiply_int function with the given num and multiplier arguments
    print(result)  # Print the result of the multiplication
    assert (
        result == expected_result
    ), f"AssertionError: Expected the output to be {expected_result}"  # Assert that the result of the multiplication is equal to the expected_result

if __name__ == "__main__":   # Check if the script is being run as the main program
    # test the trivial case
    num = 4  # Define the num argument
    multiplier = 2  # Define the multiplier argument
    expected_result = 8  # Define the expected_result argument
    test_multiply_int(num, multiplier, expected_result)  # Call the test_multiply_int function with the num, multiplier, and expected_result arguments
