import json
import logging
import os.path
import tempfile
from pathlib import Path
from xml.etree import ElementTree

import docx
import pytest
import yaml
from bs4 import BeautifulSoup

# Importing the functions from file_operations_utils module
from autogpt.commands.file_operations_utils import (
    decode_textual_file,
    is_file_binary_fn,
)

# Initialize the logger for the current module
logger = logging.getLogger(__name__)

# Define a plain text string
plain_text_str = "Hello, world!"

# Function to create a mock text file with the given plain text string
def mock_text_file():
    # Create a temporary file with write mode, delete=False, and .txt suffix
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
        # Write the plain text string to the file
        f.write(plain_text_str)
    # Return the name of the created file
    return f.name

# ... (Similar comments for other mock functions)

# Function to create respective file creation functions for different file extensions
def mock_file_creation_functions():
    return {
        ".txt": mock_text_file,
        ".csv": mock_csv_file,
        ".pdf": mock_pdf_file,
        ".docx": mock_docx_file,
        ".json": mock_json_file,
        ".xml": mock_xml_file,
        ".yaml": mock_yaml_file,
        ".html": mock_html_file,
        ".md": mock_md_file,
        ".tex": mock_latex_file,
    }

# Function to test parsers for different file types
@pytest.mark.parametrize(
    "file_extension, c_file_creator",
    respective_file_creation_functions.items(),
)
def test_parsers(file_extension, c_file_creator):
    # Get the file creation function for the given file extension
    created_file_path = Path(c_file_creator())
    # Open the created file in binary mode
    with open(created_file_path, "rb") as file:
        # Decode the textual content of the file
        loaded_text = decode_textual_file(file, os.path.splitext(file.name)[1], logger)

        # Assert that the loaded text contains the plain text string
        assert plain_text_str in loaded_text

        # Get the expected binary flag based on the file extension
        should_be_binary = file_extension in binary_files_extensions
        # Assert that the actual binary flag matches the expected binary flag
        assert should_be_binary == is_file_binary_fn(file)

    # Clean up the created file
    created_file_path.unlink()

# Set the respective_file_creation_functions variable to the output of mock_file_creation_functions
respective_file_creation_functions = mock_file_creation_functions()
binary_files_extensions = [".pdf", ".docx"]
