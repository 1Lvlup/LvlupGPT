import subprocess
import pytest


def run_game_with_inputs(inputs):
    # Start the game process
    process = subprocess.Popen(
        ["python", "tic_tac_toe.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    # Send the input moves one by one
    for move in inputs:
        output = process.communicate(move + "\n")[0]
        if process.returncode != 0:
            raise subprocess.CalledProcessError(process.returncode, "tic_tac_toe.py", output)

    # Get the final output
    output, errors = process.communicate()

    # Print the inputs and outputs
    print("Inputs:\n", "\n".join(inputs))
    print("Output:\n", output)
    print("Errors:\n", errors)

    return output


@pytest.fixture
def game_process():
    process = subprocess.Popen(
        ["python", "tic_tac_toe.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    yield process

    # Terminate the process after the test
    process.terminate()


def test_game(game_process, inputs, expected_output):
    # Send the input moves one by one
    for move in inputs:
        output = game_process.communicate(move + "\n")[0]
        if game_process.returncode != 0:
            raise subprocess.CalledProcessError(game_process.returncode, "tic_tac_toe.py", output)

    # Get the final output
    output, errors = game_process.communicate()

    # Print the inputs and outputs
    print("
