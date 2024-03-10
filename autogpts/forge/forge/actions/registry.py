import glob
import importlib
import inspect
import os
from typing import Any, Callable, Dict, List, Optional

import pydantic


class ActionParameter(pydantic.BaseModel):
    name: str
    description: str
    type_: str
    required: bool


class Action(pydantic.BaseModel):
    name: str
    description: str
    method: Callable
    parameters: List[ActionParameter]
    output_type: str
    category: Optional[str] = None

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return self.method(*args, **kwds)

    def __str__(self) -> str:
        params_str = ", ".join(
            f"{param.name}: {param.type_}" for param in self.parameters
        )
        return f"{self.name}({params_str}) -> {self.output_type}. Usage: {self.description}."


def action(
    name: str, description: str, parameters: List[ActionParameter], output_type: str
):
    def decorator(func):
        func_params = inspect.signature(func).parameters
        param_names = {param.name for param in parameters}
        param_names.update(["agent", "task_id"])
        func_param_names = set(func_params.keys())

        if param_names != func_param_names:
            raise ValueError(
                f"Mismatch in parameter names. Action Annotation includes {param_names}, but function actually takes {func_param_names} in function {func.__name__} signature"
            )

        func.action = Action(
            name=name,
            description=description,
            parameters=parameters,
            method=func,
            output_type=output_type,
        )
        return func

    return decorator


class ActionRegister:
    def __init__(self, agent=None):
        self.abilities = {}
        self.register_abilities()
        self.agent = agent

    def register_abilities(self):
        action_module_path = os.path.join(os.path.dirname(__file__), "actions")
        for action_path in glob.glob(os.path.join(action_module_path, "*.py")):
            if not os.path.basename(action_path) in ["__init__.py", "registry.py"]:
                action_module_name = os.path.relpath(
                    action_path, os.path.dirname(action_module_path)
                ).replace(os.sep, ".")[:-3]

                try:
                    module = importlib.import_module(f"forge.actions.{action_module_name}")
                    for attr in dir(module):
                        func = getattr(module, attr)
                        if hasattr(func, "action"):
                            ability = func.action
                            ability.category = (
                                action_module_name.lower().replace("_", " ")
                                if "." in action_module_name
                                else "general"
                            )
                            self.abilities[func.action.name] = ability
                except Exception as e:
                    print(f"Error occurred while registering abilities: {str(e)}")

    def list_abilities(self) -> List[Action]:
        return list(self.abilities.values())

    def list_abilities_for_prompt(self) -> List[str]:
        return [str(action) for action in self.abilities.values()]

    def abilities_description(self) -> str:
        abilities_by_category = {}
        for action in self.abilities.values():
            if action.category not in abilities_by_category:
                abilities_by_category[action.category] = []
            abilities_by_category[action.category].append(str(action))

        abilities_description = ""
        for category, actions in abilities_by_category.items():
            if abilities_description != "":
                abilities_description += "\n"
            abilities_description += f"{category}:"
            for action in actions:
                abilities_description += f"  {action}"

        return abilities_description

    async def run_action(
        self, task_id: str, action_name: str, *args: Any, **kwds: Any
    ) -> Any:
        try:
            action = self.abilities[action_name]
            return await action(self.agent, task_id, *args, **kwds)
        except Exception as e:
            raise e


if __name__ == "__main__":
    import sys

    sys.path.append("/Users/swifty/dev/forge/forge")
    register = ActionRegister(agent=None)
    print(register.abilities_description())
    print(register.run_action("abc", "list_files", "/Users/swifty/dev/forge/forge"))
