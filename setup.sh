#!/bin/bash  <-- This line is called a shebang and it specifies the interpreter used to run this script

if [[ "$OSTYPE" == "cygwin" ]] || [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    # This block checks if the system is running on Windows. If it is, the script will print an error message and exit with a status of 1
    echo "This script cannot be run on Windows."
    echo "Please follow the installation instructions at https://docs.python.org/3/using/windows.html"
    echo "To install poetry on Windows, please follow the instructions at https://python-poetry.org/docs/master/#installation"
    
    exit 1
else
    # This block runs if the system is not running on Windows
    if ! command -v python3 &> /dev/null; then
        # This block checks if python3 is installed. If not, it installs python3 using pyenv
        echo "python3 could not be found"
        echo "Installing python3 using pyenv..."
        if ! command -v pyenv &> /dev/null; then
            # This block checks if pyenv is installed. If not, it installs pyenv
            echo "pyenv could not be found"
            echo "Installing pyenv..."
            curl https://pyenv.run | bash
        fi
        pyenv install 3.11.5  # Installs python version 3.11.5
        pyenv global 3.11.5  # Sets the global python version to 3.11.5
    fi

    if ! command -v poetry &> /dev/null; then
        # This block checks if Poetry is installed. If not, it installs Poetry
        echo "poetry could not be found"
        echo "Installing poetry..."
        curl -sSL https://install.python-poetry.org | python3 -
