import pytest
from abstract_class import ShipPlacement, Turn
from battleship import Battleship

@pytest.fixture
def battleship_game():
    """
    A pytest fixture to create a new instance of the Battleship game.

    Returns:
        Battleship: A new Battleship game instance.
    """
    return Battleship()


@pytest.fixture
def initialize_game(battleship_game):
    """
    A pytest fixture to initialize a Battleship game instance with given ship placements.

    If no ship placements are provided, default ship placements will be used.

    Args:
        battleship_game (Battleship): A Battleship game instance.

    Yields:
        str: The ID of the initialized game.

    """
    def game_initializer(ship_placements=None):
        # Create a game instance
        game_id = battleship_game.create_game()

        # Place all the ships using battleship_game's methods
        if ship_placements is None:
            ship_placements = [
                ShipPlacement(ship_type, (row, column), "horizontal")
                for row, column, ship_type in [
                    (1, "A", "carrier"),
                    (2, "A", "battleship"),
                    (3, "A", "cruiser"),
                    (4, "A", "submarine"),
                    (5, "A", "destroyer"),
                ]
            ]

        for ship_placement in ship_placements:
            battleship_game.create_ship_placement(game_id, ship_placement)

        return game_id

    return game_initializer


@pytest.fixture
def game_over_fixture(battleship_game, initialize_game):
    """
    A pytest fixture to simulate a game over state in a Battleship game instance.

    Args:
        battleship_game (Battleship):
