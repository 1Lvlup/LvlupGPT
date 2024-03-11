from .registry import Action, ActionParameter, ActionRegister, action  # Importing necessary modules from the registry

# Define a new action using the 'action' decorator
@action
# Define the action's parameters
@ActionRegister.parameter(ActionParameter('parameter_name', str, 'The description of the parameter'))
def my_action(parameter_name):
    """
    This is the docstring for my_action.
    It should provide a brief description of what the function does,
    as well as any relevant information about its input and output.

    :param parameter_name: The description of the parameter
    :type parameter_name: str
    """
    # Function implementation goes here
    pass
