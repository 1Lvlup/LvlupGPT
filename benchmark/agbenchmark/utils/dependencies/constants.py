"""Module constants for test markers.

This module contains constants used for defining test markers in a test suite.
"""

# Marker name: The name of the marker used to identify dependent tests
MARKER_NAME = "depends"

# Marker keywords: A dictionary of keyword arguments for the marker
MARKER_KWARGS = {
    # The 'names' keyword argument represents custom names for the tests
    "names": "Custom names for the tests. Default is 'test'.",
    
    # The 'depends_on' keyword argument represents tests to depend on
    "depends_on": "Tests to depend on. Default is ()."
}

# Default value for the 'names' keyword argument
MARKER_KWARG_DEFAULT_NAME = "test"

# Default value for the 'depends_on' keyword argument
MARKER_KWARG_DEFAULT_DEPENDENCIES = ()

