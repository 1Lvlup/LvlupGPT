from autogpt.command_decorator import command  # Importing the command decorator from autogpt package
from autogpt.core.utils.json_schema import JSONSchema  # Importing JSONSchema for input argument validation

# Define the category for the command
COMMAND_CATEGORY = "mock"


@command(  # Decorator for creating a command
    "function_based_cmd",  # Name of the command
    "Function-based test command",  # Description of the command
    {
        "arg1": JSONSchema(  # Schema for the first argument
            type=JSONSchema.Type.INTEGER,  # Argument type is integer
            description="arg 1",  # Description of the argument
            required=True,  # Argument is required
        ),
        "arg2": JSONSchema(  # Schema for the second argument
            type=JSONSchema.Type.STRING,  # Argument type is string
            description="arg 2",  # Description of the argument
            required=True,  # Argument is required
        ),
    },
)
def function_based_cmd(arg1: int, arg2: str) -> str:
    """A function-based test command.

    This function takes two arguments, an integer and a string, and returns a string
    with the two arguments separated by a dash.

    Args:
        arg1 (int): The first argument, an integer.
        arg2 (str): The second argument, a string.

    Returns:
        str: The two arguments separated by a dash.
    """
    return f"{arg1} - {arg2}"  # Concatenate the two arguments with a dash in between
