from __future__ import annotations

import logging
from colorama import Fore, Style

SIMPLE_LOG_FORMAT = "[%(asctime)s] %(levelname)s %(message)s"
DEBUG_LOG_FORMAT = "[%(asctime)s] %(levelname)s %(filename)s:%(lineno)03d  %(message)s"

def configure_logging(level: int = logging.INFO) -> None:
    """Configure the native logging module."""

    log_format = DEBUG_LOG_FORMAT if level == logging.DEBUG else SIMPLE_LOG_FORMAT

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(FancyConsoleFormatter(log_format))

    logging.basicConfig(
        level=level,
        format=log_format,
        handlers=[console_handler],
    )

class FancyConsoleFormatter(logging.Formatter):
    """
    A custom logging formatter designed for console output.

    This formatter enhances the standard logging output with color coding. The color
    coding is based on the level of the log message, making it easier to distinguish
    between different types of messages in the console output.

    The color for each level is defined in the LEVEL_COLOR_MAP class attribute.
    """

    LEVEL_COLOR_MAP = {
        logging.DEBUG: {"color": Fore.LIGHTBLACK_EX, "bold": False},
        logging.INFO: {"color": Fore.BLUE, "bold": False},
        logging.WARNING: {"color": Fore.YELLOW, "bold": False},
        logging.ERROR: {"color": Fore.RED, "bold": False},
        logging.CRITICAL: {"color": Fore.RED + Style.BRIGHT, "bold": True},
    }

    def format(self, record: logging.LogRecord) -> str:
        # Make sure `msg` is a string
        if not hasattr(record, "msg"):
            record.msg = ""
        elif not type(record.msg) is str:
            record.msg = str(record.msg)

        # Justify the level name to 5 characters minimum
        record.levelname = record.levelname.ljust(5)

        # Determine color and bold based on error level
        level_color = self.LEVEL_COLOR_MAP.get(record.levelno)
        if level_color:
            record.levelname = f"{level_color['color']}{record.levelname}{Style.RESET_ALL}"
            record.msg = f"{level_color['color']}{record.msg}{Style.RESET_ALL}"
            record.bold = level_color["bold"]

        # Determine color for message
        color = getattr(record, "color", level_color["color"]) if record.bold else ""

        # Don't color INFO messages unless the color is explicitly specified.
        if color and (record.levelno != logging.INFO or hasattr(record, "color")):
            record.msg = f"{color}{record.msg}{Style.RESET_ALL}"

        return super().format(record)
