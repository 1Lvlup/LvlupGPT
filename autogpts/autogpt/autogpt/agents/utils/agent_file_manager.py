from __future__ import annotations

import logging
import os
from pathlib import Path

logger = logging.getLogger(__name__)

class AgentFileManager:
    """A class that represents a workspace for an AutoGPT agent."""

    def __init__(self, agent_data_dir: Path):
        self.root = agent_data_dir.resolve()
        self.state_file_path = self.root / "state.json"
        self.file_ops_log_path = self.root / "file_logger.log"

    def __str__(self) -> str:
        return f"AgentFileManager(root={self.root}, state_file_path={self.state_file_path}, file_ops_log_path={self.file_ops_log_path})"

    def initialize(self) -> None:
        try:
            self.root.mkdir(parents=True, exist_ok=True)
            self.init_file_ops_log()
        except Exception as e:
            logger.error(f"Error initializing AgentFileManager: {e}")

    def init_file_ops_log(self) -> None:
        try:
            if not self.file_ops_log_path.exists():
                with self.file_ops_log_path.open(mode="w", encoding="utf-8") as f:
                    f.write("")
        except Exception as e:
            logger.error(f"Error initializing file operations log: {e}")
