#!/usr/bin/env bash

function find_python_command() {
    if command -v python3 &> /dev/null
    then
        echo "python3"
    elif command -v python &> /dev/null
    then
        echo "python"
    else
        echo "Python not found. Please install Python."
        exit 1
    fi
}

function find_poetry_command() {
    if command -v poetry &> /dev/null
    then
        echo "poetry"
    else
        echo "Poetry not found. Please install Poetry."
        exit 1
    fi
}

PYTHON_CMD=$(find_python_command)
POETRY_CMD=$(find_poetry_command)

if $PYTHON_CMD -c "import sys; sys.version_info < (3, 10)"; then
    echo "Python 3.10 or higher is required to run Auto GPT."
    exit 1
fi

if ! $PYTHON_CMD -c "import sys; import check_requirements; check_requirements.main()"; then
    echo
    $POETRY_CMD install --no-cache-dir --quiet
    echo
    echo "Finished installing packages! Starting AutoGPT..."
    echo
fi

$POETRY_CMD run autogpt "$@"
