import pytest
from autogpt.models.base_open_ai_plugin import BaseOpenAIPlugin


class DummyPlugin(BaseOpenAIPlugin):
    """A dummy plugin for testing purposes."""


@pytest.fixture
def dummy_plugin():
    """A dummy plugin for testing purposes."""
    manifests_specs_clients = {
        "manifest": {
            "name_for_model": "Dummy",
            "schema_version": "1.0",
            "description_for_model": "A dummy plugin for testing purposes",
        },
        "client": None,
        "openapi_spec": None,
    }
    return DummyPlugin(manifests_specs_clients)


@pytest.mark.unit
def test_dummy_plugin_inheritance(dummy_plugin: BaseOpenAIPlugin):
    """Test that the DummyPlugin class inherits from the BaseOpenAIPlugin class."""
    assert isinstance(dummy_plugin, BaseOpenAIPlugin)


@pytest.mark.unit
def test_dummy_plugin_properties(dummy_plugin: DummyPlugin):
    """Test that the DummyPlugin class has the correct properties."""
    assert dummy_plugin._name == "Dummy"
    assert dummy_plugin._version == "1.0"
    assert dummy_plugin._description == "A dummy plugin for testing purposes"


@pytest.mark.unit
def test_dummy_plugin_default_methods(dummy_plugin: DummyPlugin):
    """Test that the DummyPlugin class has the correct default methods."""
    with pytest.raises(NotImplementedError):
        dummy_plugin.can_handle_on_response()

    with pytest.raises(NotImplementedError):
        dummy_plugin.can_handle_post_prompt()

    with pytest.raises(NotImplementedError):
        dummy_plugin.can_handle_on_planning()

    with pytest.raises(NotImplementedError):
        dummy_plugin.can_handle_post_planning()

    with pytest.raises(NotImplementedError):
        dummy_plugin.can_handle_pre_instruction()

    with pytest.raises(NotImplementedError):
        dummy_plugin.can_handle_on_instruction()

    with pytest.raises(NotImplementedError):
        dummy_plugin.can_handle_post_instruction()

    with pytest.raises(NotImplementedError):
        dummy_plugin.can_handle_pre_command()

    with pytest.raises(NotImplementedError):
        dummy_plugin.can_handle_post_command()

    with pytest.raises(NotImplementedError):
        dummy_plugin.can_handle_chat_completion(None, None, None, None)

    with pytest.raises(NotImplementedError):
        dummy_plugin.can_handle_text_embedding(None)

    assert dummy_plugin.on_response("hello") == "hello"
    assert dummy_plugin.post_prompt(None) is None
    assert dummy_plugin.on_planning(None, None) is None
    assert dummy_plugin.post_planning("world") == "world"
    pre_instruction = dummy_plugin.pre_instruction(
        [{"role": "system", "content": "Beep, bop, boop"}]
    )
    assert isinstance(pre_instruction, list)
    assert len(pre_instruction) == 1
    assert pre_instruction[0]["role"] == "system"
    assert pre_instruction[0]["content"] == "Beep, bop, boop"
    assert dummy_plugin.on_instruction(None) is None
    assert dummy_plugin.post_instruction("I'm a robot") == "I'm a robot"
    pre_command = dummy_plugin.pre_command("evolve", {"continuously": True})
    assert isinstance(pre_command, tuple)
    assert len(pre_command) == 2
    assert pre_command[0] == "evolve"
    assert pre_command[1]["continuously"] is True
    post_command = dummy_plugin.post_command("evolve", "upgraded successfully!")
    assert isinstance(post_command, str)
    assert post_command == "upgraded successfully!"
    assert dummy_plugin.handle_chat_completion(None, None, None, None) is None
    assert dummy_plugin.handle_text_embedding(None) is None
