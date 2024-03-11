import time

from autogpt.app.spinner import Spinner

# A constant message indicating that the task is almost done
ALMOST_DONE_MESSAGE = "Almost done..."
# A constant message indicating that the user should wait
PLEASE_WAIT = "Please wait..."

def test_spinner_initializes_with_default_values():
    """
    Tests that the spinner initializes with default values.
    This function tests the initialization of the Spinner class with default values for message and delay.
    """
    with Spinner() as spinner:
        # Assert that the default message is set to "Loading..."
        assert spinner.message == "Loading..."
        # Assert that the default delay is set to 0.1 seconds
        assert spinner.delay == 0.1

def test_spinner_initializes_with_custom_values():
    """
    Tests that the spinner initializes with custom message and delay values.
    This function tests the initialization of the Spinner class with custom values for message and delay.
    """
    with Spinner(message=PLEASE_WAIT, delay=0.2) as spinner:
        # Assert that the custom message is set correctly
        assert spinner.message == PLEASE_WAIT
        # Assert that the custom delay is set correctly
        assert spinner.delay == 0.2

def test_spinner_stops_spinning():
    """
    Tests that the spinner starts spinning and stops spinning without errors.
    This function tests whether the spinner can be started and stopped without raising any exceptions.
    """
    with Spinner() as spinner:
        # Simulate the passage of time to allow the spinner to spin
        time.sleep(1)
    # Assert that the spinner has stopped spinning
    assert not spinner.running

def test_spinner_can_be_used_as_context_manager():
    """
    Tests that the spinner can be used as a context manager.
    This function tests whether the spinner can be used as a context manager, ensuring that it starts and stops spinning as expected.
    """
    with Spinner() as sp
