from __future__ import annotations

import logging
from contextlib import ExitStack
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..base import BaseAgentConfiguration  # Imported only for type checking

from autogpt.models.action_history import EpisodicActionHistory  # Imported only for type checking

from ..base import BaseAgent  # Imported only for type checking

logger = logging.getLogger(__name__)  # Create a logger for the module


class WatchdogMixin:
    """
    Mixin that adds a watchdog feature to an agent class. Whenever the agent starts
    looping, the watchdog will switch from the FAST_LLM to the SMART_LLM and re-think.
    """

    config: BaseAgentConfiguration  # Configuration object for the agent
    event_history: EpisodicActionHistory  # History of actions taken by the agent

    def __init__(self, **kwargs) -> None:
        # Initialize other bases first, because we need the event_history from BaseAgent
        super(WatchdogMixin, self).__init__(**kwargs)

        if not isinstance(self, BaseAgent):
            raise NotImplementedError(
                f"{__class__.__name__} can only be applied to BaseAgent derivatives"
            )

    async def propose_action(
        self, *args, **kwargs
    ) -> BaseAgent.ThoughtProcessOutput:
        """
        Overridden method that provides the watchdog feature. It first calls the
        propose_action method of the base class and checks if the conditions for
        switching the language model are met. If so, it switches to the SMART_LLM and
        re-thinks the action.
        """
        command_name, command_args, thoughts = await super(
            WatchdogMixin, self
        ).propose_action(*args, **kwargs)

        if not self.config.big_brain and self.config.fast_llm != self.config.smart_llm:
            # Check if the conditions for switching the language model are met
            previous_command, previous_command_args = None, None
            if len(self.event_history) > 1:
                # Detect repetitive commands
                previous_cycle = self.event_history.episodes[
                    self.event_history.cursor - 1
                ]
                previous_command = previous_cycle.action.name
                previous_command_args = previous_cycle.action.args

            rethink_reason = ""

            if not command_name:
                rethink_reason = "AI did not specify a command"
            elif (
                command_name == previous_command
                and command_args == previous_command_args
            ):
                rethink_reason = f"Repititive command detected ({command_name})"

            if rethink_reason:
                logger.info(f"{rethink_reason}, re-thinking with SMART_LLM...")
                with ExitStack() as stack:

                    @stack.callback
                    def restore_state() -> None:
                        # Executed after exiting the ExitStack context
                        self.config.big_brain = False

                    # Remove partial record of current cycle
                    self.event_history.rew
