from fastapi import FastAPI  # Importing FastAPI module


class AgentMiddleware:
    """
    Middleware that injects the agent instance into the request scope.
    This class is a middleware that, when added to the FastAPI app, will inject
    the 'agent' instance into the request scope, making it accessible within
    the request handling function.
    """

    def __init__(self, app: FastAPI, agent: "Agent"):
        """
        Initializes the AgentMiddleware class with the FastAPI app and agent instance.

        Args:
            app (FastAPI): The FastAPI app - automatically injected by FastAPI.
            agent (Agent): The agent instance to inject into the request scope.

        Examples:
            >>> from fastapi import FastAPI, Request
            >>> from agent_protocol.agent import Agent
            >>> from agent_protocol.middlewares import AgentMiddleware
            >>> app = FastAPI()
            >>> @app.get("/")
            >>> async def root(request: Request):
            >>>     agent = request["agent"]
            >>>     task = agent.db.create_task("Do something.")
            >>>     return {"task_id": a.task_id}
            >>> agent = Agent()
            >>> app.add_middleware(AgentMiddleware, agent=agent)
        """
        self.app = app  # Assigning the FastAPI app to the 'app' attribute
        self.agent = agent  # Assigning the agent instance to the 'agent' attribute

    async def __call__(self, scope, receive, send):
        """
        The main function that gets called when this middleware is invoked.

        Args:
            scope (dict): A dictionary containing information about the current request.
            receive (callable): A callable used to receive messages from the FastAPI app.
            send (callable): A callable used to send messages to the FastAPI app.

        This function injects the 'agent' instance into the 'scope' dictionary,
        making it accessible within the request handling function.
        """
        scope["agent"] = self.agent  # Injecting the 'agent' instance into the 'scope' dictionary

