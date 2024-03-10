from __future__ import annotations
from typing import List, Any

from autogpt.core.prompting import ChatPrompt, ChatMessage
from autogpt.models.context_item import ContextItem
from autogpt.core.resource.model_providers import BaseModelProvider


class AgentContext:
    def __init__(self, items: List[ContextItem] = None):
        self.items = items or []

    def __bool__(self) -> bool:
        return bool(self.items)

    def __contains__(self, item: ContextItem) -> bool:
        return any(i.source == item.source for i in self.items)

    def add(self, item: ContextItem) -> None:
        self.items.append(item)

    def close(self, index: int) -> None:
        self.items.pop(index - 1)

    def clear(self) -> None:
        self.items.clear()

    def format_numbered(self) -> str:
        return "\n\n".join([f"{i}. {c.fmt()}" for i, c in enumerate(self.items, 1)])


class ContextMixin:
    """Mixin that adds context support to a BaseAgent subclass"""

    context: AgentContext

    def __init__(self, **kwargs: Any):
        self.context = AgentContext()
        super().__init__(**kwargs)

    def build_prompt(
        self,
        *args: Any,
        extra_messages: List[ChatMessage] = None,
        **kwargs: Any,
    ) -> ChatPrompt:
        """Builds a chat prompt with the current agent context.

        Args:
            *args: Variable length argument list.
            extra_messages: Additional messages to include in the prompt.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            ChatPrompt: The built chat prompt.
        """
        if not extra_messages:
            extra_messages = []

        if self.context:
            extra_messages.insert(
                0,
                ChatMessage.system(
                    "## Context\n"
                    f"{self.context.format_numbered()}\n\n"
                    "When a context item is no longer needed and you are not done yet, "
                    "you can hide the item by specifying its number in the list above "
                    "to `hide_context_item`.",
                ),
            )

        return ChatPrompt(*args, extra_messages=extra_messages, **kwargs)


def get_agent_context(agent: BaseModelProvider) -> AgentContext:
    if isinstance(agent, ContextMixin):
        return agent.context

    return AgentContext()
