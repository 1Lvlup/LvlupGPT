from forge.actions import ActionRegister  # ActionRegister is used to manage custom actions for the agent.
from forge.sdk import (  # The forge.sdk module contains core classes and functions for building agents.
    Agent,
    AgentDB,
    ForgeLogger,
    Step,
    StepRequestBody,
    Task,
    TaskRequestBody,
    Workspace,
)

class ForgeAgent(Agent):
    """
    The ForgeAgent class is a customizable agent for the Forge framework. It provides a basic structure for handling tasks, steps, and actions.
    """

    def __init__(self, database: AgentDB, workspace: Workspace):
        """
        Initialize the ForgeAgent with a database and workspace.

        :param database: An instance of AgentDB for storing tasks, steps, and artifact metadata.
        :param workspace: A Workspace instance for storing and managing artifacts.
        """
        super().__init__(database, workspace)
        self.abilities = ActionRegister(self)  # Initialize the ActionRegister to manage custom actions.

    async def create_task(self, task_request: TaskRequestBody) -> Task:
        """
        Create a new task and log a message.

        :param task_request: The request body containing task information.
        :return: A Task object representing the newly created task.
        """
        task = await super().create_task(task_request)
        LOG.info(f"Task created: {task.task_id}...")
        return task

    async def execute_step(self, task_id: str, step_request: StepRequestBody) -> Step:
        """
        Execute a step for a specific task, perform any necessary actions, and return a Step object with the output.

        :param task_id: The ID of the task associated with the step.
        :param step_request: The request body containing step information.
        :return: A Step object representing the completed step.
        """
        step = await self.db.create_step(task_id=task_id, input=step_request, is_last=True)
        self.workspace.write(task_id=task_id, path="output.txt", data=b"Washington D.C")
        await self.db.create_artifact(
            task_id=task_id,
            step_id=step.step_id,
            file_name="output.txt",
            relative_path="",
            agent_created=True,
        )
        step.output = "Washington D.C"
        LOG.info(
            f"Final Step completed: {step.step_id}.\n"
            f"Output should be placeholder text Washington D.C. You'll need to\n"
            f"modify execute_step to include LLM behavior. Follow the tutorial "
            f"if confused. "
        )
        return step
