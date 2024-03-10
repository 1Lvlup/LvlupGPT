from __future__ import annotations

import os
import uuid
from pathlib import Path
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from autogpt.agents.agent import AgentSettings

class AgentFileManager:
    def __init__(self, agent_dir: Path):
        self.agent_dir = agent_dir

    @property
    def state_file_path(self) -> Path:
        return self.agent_dir / "state.json"

    def load_state_from_json_file(self) -> AgentSettings:
        # Implement this method to load AgentSettings from state.json
        pass

class AgentManager:
    def __init__(self, app_data_dir: Path):
        self.app_data_dir = app_data_dir
        self.agents_dir = self.app_data_dir / "agents"
        self.agents_dir.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def generate_id(agent_name: str) -> str:
        unique_id = str(uuid.uuid4())[:8]
        return f"{agent_name}-{unique_id}"

    def list_agents(self) -> List[str]:
        agent_dirs = [d for d in self.agents_dir.iterdir() if d.is_dir()]
        return [d.name for d in agent_dirs if self._is_agent_initialized(d)]

    def _is_agent_initialized(self, agent_dir: Path) -> bool:
        state_file_path = AgentFileManager(agent_dir).state_file_path
        return state_file_path.exists()

    def get_agent_dir(self, agent_id: str, must_exist: bool = False) -> Path:
        agent_dir = self.agents_dir / agent_id
        if must_exist and not agent_dir.exists():
            raise FileNotFoundError(f"No agent with ID '{agent_id}'")
        return agent_dir

    def retrieve_state(self, agent_id: str) -> AgentSettings:
        agent_dir = self.get_agent_dir(agent_id, True)
        state_file = AgentFileManager(agent_dir).state_file_path
        if not state_file.exists():
            raise FileNotFoundError(f"Agent with ID '{agent_id}' has no state.json")

        state = AgentFileManager(agent_dir).load_state_from_json_file()
        state.agent_data_dir = agent_dir
       
