import os
import random
import sys

if "pytest" in sys.argv or "pytest" in sys.modules or os.getenv("CI"):
    # Check if the code is being run by pytest or in a continuous integration environment
    # If so, set the random seed to 42 for consistency in test results
    random.seed(42)
