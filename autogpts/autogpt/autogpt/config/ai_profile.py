from pathlib import Path
import yaml
from typing import List, Union
from pydantic import BaseModel, Field

class AIProfile(BaseModel):
    """
    Object to hold the AI's personality.

    Attributes:
        ai_name (str): The name of the AI.
        ai_role (str): The description of the AI's role.
        ai_goals (List[str]): The list of objectives the AI is supposed to complete.
        api_budget (float): The maximum dollar value for API calls (0.0 means infinite)
    """

    ai_name: str = Field(default="")
    ai_role: str = Field(default="")
    ai_goals: List[str] = Field(default_factory=list)
    api_budget: float = Field(default=0.0)

    @staticmethod
    def load(ai_settings_file: Union[str, Path]) -> "AIProfile":
        """
        Returns class object with parameters (ai_name, ai_role, ai_goals, api_budget)
        loaded from yaml file if it exists, else returns class with no parameters.

        Parameters:
            ai_settings_file (Union[str, Path]): The path to the config yaml file.

        Returns:
            cls (object): An instance of given cls object
        """

        config_params: dict = {}

        if isinstance(ai_settings_file, str):
            ai_settings_file = Path(ai_settings_file)

        if ai_settings_file.exists():
            with ai_settings_file.open(encoding="utf-8") as file:
                try:
                    config_params = yaml.load(file, Loader=yaml.FullLoader) or {}
                except yaml.YAMLError as exc:
                    print(f"Error loading yaml file: {exc}")

        ai_name = config_params.get("ai_name", "")
        ai_role = config_params.get("ai_role", "")
        ai_goals = [
            str(goal).strip("{}").replace("'", "").replace('"', "")
            if isinstance(goal, dict)
            else str(goal)
            for goal in config_params.get("ai_goals", [])
        ]
        api_budget = config_params.get("api_budget", 0.0)

        return AIProfile(
            ai_name=ai_name, ai_role=ai_role, ai_goals=ai_goals, api_budget=api_budget
        )

    def save(self, ai_settings_file: Union[str, Path]) -> None:
        """
        Saves the class parameters to the specified file yaml file path as a yaml file.

        Parameters:
            ai_settings_file (Union[str, Path]): The path to the config yaml file.

        Returns:
            None
        """

        if isinstance(ai_settings_file, str):
            ai_settings_file = Path(ai_settings_file)

        with ai_settings_file.open("w", encoding="utf-8") as file:
            yaml.dump(self.dict(), file, allow_unicode=True)
