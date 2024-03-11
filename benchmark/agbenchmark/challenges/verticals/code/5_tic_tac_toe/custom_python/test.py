import subprocess
import pytest

def run_game_with_inputs(inputs):
    # Start the game process using the tic_tac_toe.py script
    process = subprocess.Popen(
        ["python", "tic_tac_toe.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    # Send the input moves one by one to the game process
    for move in inputs:
        output = process.communicate(move + "\n")[0]

        # Check if the game process has returned a non-zero exit code
        if process.returncode != 0:
            raise subprocess.CalledProcessError(process.returncode, "tic_tac_toe.py", output)

    # Get the final output and errors from the game process
    output, errors = process.communicate()

    # Print the inputs, output, and errors for debugging purposes
    print("Inputs:\n", "\n".join(inputs))
    print("Output:\n", output)
    print("Errors:\n", errors)

    return output

@pytest.fixture
def game_process():
    # Start the game process using the tic_tac_toe.py script
    process = subprocess.Popen(
        ["python", "tic_tac_toe.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    # Yield the game process to the test function
    yield process

    # Terminate the game process after the test is complete
    process.terminate()

def test_game(game_process, inputs, expected_output):
    # Send the input moves one by one to the game process
    for move in inputs:
        output = game_process.communicate(move + "\n")[0]

        # Check if the game process has returned a non-zero exit code
        if game_process.returncode != 0:
            raise subprocess.CalledProcessError(game_process.returncode, "tic_tac_toe.py", output)

    # Get the final output and errors from the game process
    output, errors = game_process.communicate()
