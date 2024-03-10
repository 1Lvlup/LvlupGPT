"""A simple spinner module."""
import itertools
import sys
import threading
import time


class Spinner:
    """A simple spinner class.

    A spinner is a simple text-based loading indicator. This class provides a
    simple way to display a spinner with an optional message.

    Attributes:
        message (str): The message to display. Defaults to "Loading...".
        delay (float): The delay between each spinner update. Defaults to 0.1.
        plain_output (bool): Whether to display the spinner or not. Defaults to False.
        spinner (itertools.cycle): The spinner iterator.
        running (bool): Whether the spinner is running or not.
        spinner_thread (threading.Thread): The thread running the spinner.
        daemon (bool): Whether the spinner thread is a daemon or not. Defaults to False.

    """

    def __init__(
        self,
        message: str = "Loading...",
        delay: float = 0.1,
        plain_output: bool = False,
    ) -> None:
        """Initialize the spinner class.

        Args:
            message (str): The message to display.
            delay (float): The delay between each spinner update.
            plain_output (bool): Whether to display the spinner or not.

        """
        self.plain_output = plain_output
        self.spinner = itertools.cycle(["-", "/", "|", "\\"])
        self.delay = delay
        self.message = message
        self.running = False
        self.spinner_thread = None
        self.daemon = False

    def spin(self) -> None:
        """Spin the spinner."""
        if self.plain_output:
            self.print_message()
            return
        while self.running:
            self.print_message()
            time.sleep(self.delay)

    def print_message(self):
        """Print the spinner message."""
        sys.stdout.write(f"\r{' ' * (len(self.message) + 2)}\r")
        sys.stdout.write(f"{next(self.spinner)} {self.message}\r")
        sys.stdout.flush()

    def pause(self):
        """Pause the spinner."""
        self.running = False

    def resume(self):
        """Resume the spinner."""
        self.running = True
        self.spinner_thread = threading.Thread(target=self.spin)
        self.spinner_thread.start()

    def start(self):
        """Start the spinner."""
        self.running = True
        self.spinner_thread =
