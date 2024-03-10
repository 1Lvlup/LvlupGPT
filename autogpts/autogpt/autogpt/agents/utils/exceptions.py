from typing import Optional

class AgentException(Exception):
    """Base class for specific exceptions relevant in the execution of Agents"""

    def __init__(self, message: str, hint: Optional[str] = None):
        self.message = message
        self.hint = hint

    def __str__(self):
        return f'AgentException: {self.message}\nHint: {self.hint}'

class AgentTerminated(AgentException):
    """The agent terminated or was terminated"""
    def __init__(self, message: str):
        super().__init__(message=message, hint=None)

class ConfigurationError(AgentException):
    """Error caused by invalid, incompatible or otherwise incorrect configuration"""
    def __init__(self, message: str):
        super().__init__(message=message, hint="Check the configuration and try again.")

class InvalidAgentResponseError(AgentException):
    """The LLM deviated from the prescribed response format"""
    def __init__(self, message: str):
        super().__init__(message=message, hint="Ensure the LLM follows the correct response format.")

class UnknownCommandError(AgentException):
    """The AI tried to use an unknown command"""
    def __init__(self, message: str):
        super().__init__(message=message, hint="Do not try to use this command again.")

class DuplicateOperationError(AgentException):
    """The proposed operation has already been executed"""
    def __init__(self, message: str):
        super().__init__(message=message, hint="The operation has already been executed.")

class CommandExecutionError(AgentException):
    """An error occurred when trying to execute the command"""
    def __init__(self, message: str):
        super().__init__(message=message, hint=None)

class InvalidArgumentError(CommandExecutionError):
    """The command received an invalid argument"""
    def __init__(self, message: str):
        super().__init__(message=message, hint="Check the command arguments and try again.")

class OperationNotAllowedError(CommandExecutionError):
    """The agent is not allowed to execute the proposed operation"""
    def __init__(self, message: str):
        super().__init__(message=message, hint="The agent does not have permission to execute this operation.")

class AccessDeniedError(CommandExecutionError):
    """The operation failed because access to a required resource was denied"""
    def __init__(self, message: str):
        super().__init__(message=message, hint="Access to the
