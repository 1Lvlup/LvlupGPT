import pytest
from pytest_mock import MockerFixture

from autogpt.core.resource.model_providers import (
    OPEN_AI_CHAT_MODELS,
    OPEN_AI_EMBEDDING_MODELS,
)
from autogpt.llm.api_manager import ApiManager  # A class for managing API costs and budget

@pytest.fixture(autouse=True)
def api_manager():  # Fixture to create an instance of ApiManager for testing
    yield ApiManager()


@pytest.fixture(autouse=True)
def reset_api_manager(api_manager):  # Fixture to reset the ApiManager instance after each test
    api_manager.reset()


@pytest.fixture(autouse=True)
def mock_costs(mocker: MockerFixture, api_manager):  # Fixture to mock costs for models
    mocker.patch.multiple(
        OPEN_AI_CHAT_MODELS["gpt-3.5-turbo"],  # Mocking the chat model
        prompt_token_cost=0.0013,
        completion_token_cost=0.0025,
    )
    mocker.patch.multiple(
        OPEN_AI_EMBEDDING_MODELS["text-embedding-ada-002"],  # Mocking the embedding model
        prompt_token_cost=0.0004,
    )
    api_manager.update_cost(0, 0, "gpt-3.5-turbo")  # Updating the cost for the chat model
    api_manager.update_cost(0, 0, "text-embedding-ada-002")  # Updating the cost for the embedding model


class TestApiManager:  # Class for testing the ApiManager class

    @staticmethod
    def test_getter_methods(api_manager):  # Test for getter methods
        """Test the getter methods for total tokens, cost, and budget."""
        api_manager.update_cost(600, 1200, "gpt-3.5-turbo")  # Updating the cost for the chat model
        api_manager.set_total_budget(10.0)  # Setting the total budget

        total_prompt_tokens = api_manager.get_total_prompt_tokens()  # Getting the total prompt tokens
        total_completion_tokens = api_manager.get_total_completion_tokens()  # Getting the total completion tokens
        total_cost = api_manager.get_total_cost()  # Getting the total cost
        total_budget = api_manager.get_total_budget()  # Getting the total budget

        assert total_prompt_tokens == 600  # Asserting the total prompt tokens
        assert total_completion_tokens == 1200  # Asserting the total completion tokens
        assert total_cost == (600 * 0.0013 + 1200 * 0.0025) / 1000  # Asserting the total cost
        assert total_budget == 10.0  # Asserting the total budget

    @staticmethod
    def test_set_total_budget(api_manager):  # Test for setting the total budget
        """Test if setting the total budget works correctly."""
        total_budget = 10.0
        api_manager.set_total_budget(total_budget)  # Setting the total budget

        assert api_manager.get_total_budget() == total_budget  # Asserting the total budget

    @staticmethod
    def test_update_cost_completion_model(api_manager):  # Test for updating the cost for a completion model
        """Test if updating the cost works correctly."""
        prompt_tokens = 50
        completion_tokens = 100
        model = "gpt-3.5-turbo"

        api_manager.update_cost(prompt_tokens, completion_tokens, model)  # Updating the cost for the chat model

        assert api_manager.get_total_prompt_tokens() == prompt_tokens  # Asserting the total prompt tokens
        assert api_manager.get_total_completion_tokens() == completion_tokens  # Asserting the total completion tokens
        assert (
            api_manager.get_total_cost()
            == (prompt_tokens
