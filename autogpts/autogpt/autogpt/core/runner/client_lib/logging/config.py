import logging
import sys

from colorama import Fore, Style
from openai._base_client import log as openai_logger

# Define a simple log format string
SIMPLE_LOG_FORMAT = "%(asctime)s %(levelname)s  %(message)s"

# Define a more detailed debug log format string
DEBUG_LOG_FORMAT = (
    "%(asctime)s.%(msecs)03d %(levelname)s %(filename)s:%(lineno)d  %(message)s"
)

