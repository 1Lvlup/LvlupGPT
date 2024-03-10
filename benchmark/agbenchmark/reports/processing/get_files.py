import os
from typing import Tuple, List, Dict, Optional
from pathlib import Path

def get_latest_subdirectory(directory_path: str) -> Optional[str]:
    subdirs = [
        os.path.join(directory_path, name)
        for name in os.listdir(directory_path)
        if os.path.isdir(os.path.join(directory_path, name))
    ]

    if not subdirs:
        return None

    subdirs.sort(key=lambda x: os.path.getctime(x))
    return subdirs[-1]

def get_latest_reports(directory_path: str) -> List[Tuple[Path, Path]]:
    latest_reports: List[Tuple[Path, Path]] = []

    for agent_dir in os.scandir(directory_path):
        if not agent_dir.is_dir():
            continue

        latest_subdir = get_latest_subdirectory(agent_dir.path)
        if latest_subdir is None:
            continue

        report_file = latest_subdir / "report.json"
        if not report_file.is_file():
            continue

        latest_reports.append((agent_dir, report_file))

    return latest_reports
