from autogpt.config.ai_profile import AIProfile
from pathlib import Path
import yaml

def test_goals_are_always_lists_of_strings():
    """Test if the goals attribute is always a list of strings."""

    yaml_content = """
ai_goals:
  - Goal 1: Make a sandwich
    description: Making a sandwich
  - Goal 2: Eat the sandwich
    description: Eating the sandwich
  - Goal 3: Go to sleep
    description: Going to sleep
  - Goal 4: Wake up
    description: Waking up
ai_name: McFamished
ai_role: A hungry AI
api_budget: 0.0
"""

    temp_file = Path("./tmp/ai_settings.yaml")
    temp_file.write_text(yaml_content)

    ai_profile = AIProfile.load(temp_file)

    assert len(ai_profile.ai_goals) == 4
    assert ai_profile.ai_goals[0].goal == "Goal 1: Make a sandwich"
    assert ai_profile.ai_goals[0].description == "Making a sandwich"
    assert ai_profile.ai_goals[1].goal == "Goal 2: Eat the sandwich"
    assert ai_profile.ai_goals[1].description == "Eating the sandwich"
    assert ai_profile.ai_goals[2].goal == "Goal 3: Go to sleep"
    assert ai_profile.ai_goals[2].description == "Going to sleep"
    assert ai_profile.ai_goals[3].goal == "Goal 4: Wake up"
    assert ai_profile.ai_goals[3].description == "Waking up"

    temp_file.write_text("")
    ai_profile.save(temp_file)

    reloaded_ai_profile = AIProfile.load(temp_file)
    assert yaml.safe_load(temp_file.read_text()) == {
        "ai_name": "McFamished",
        "ai_role": "A hungry AI",
        "ai_goals": [
            {"goal": "Goal 1: Make a sandwich", "description": "Making a sandwich"},
            {"goal": "Goal 2: Eat the sandwich", "description": "Eating the sandwich"},
            {"goal": "Goal 3: Go to sleep", "description": "Going to sleep"},
            {"goal": "Goal 4: Wake up", "description": "Waking up"},
        ],
        "api_budget": 0.0,
    }


def test_ai_profile_file_not_exists():
    """Test if file does not exist."""

    workspace = Path("./workspace")
    ai_settings_file = workspace / "ai_settings.yaml"

    ai_profile = AIProfile.load(str(ai_settings_file))
    assert ai_profile.ai_name == ""
    assert ai_profile.ai_role == ""
    assert ai_profile.ai_goals == []
    assert ai_profile.api_budget == 0.0

