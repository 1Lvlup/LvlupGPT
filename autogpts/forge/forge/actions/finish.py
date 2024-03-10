"""
A module for the 'finish' action.
"""

from forge.sdk.forge_log import ForgeLogger
from .registry import action

logger = ForgeLogger(__name__)


@action(
    name="finish",
    description="Use this to shut down once you have accomplished all of your goals,"
    " or when there are insurmountable problems that make it impossible"
    " for you to finish your task.",
    parameters=[
        {
            "name": "reason",
            "description": "A summary to the user of how the goals were accomplished",
            "type": "string",
            "required": True,
        }
    ],
    output_type="str",
)
async def finish(
    agent: any,
    task_id: str,
    reason: str,
) -> str:
    """
    A function that takes in a string and exits the program.

    Parameters:
        agent (any): The agent object.
        task_id (str): The ID of the task.
        reason (str): A summary to the user of how the goals were accomplished.

    Returns:
        A result string from create chat completion. It is recommended to return a more informative result string,
        such as "Task '{task\_id}' has been finished with reason '{reason}'.".
    """
    logger.info(reason, extra={"title": "Shutting down...\n"})
    return f"Task '{task_id}' has been finished with reason '{reason}'."

