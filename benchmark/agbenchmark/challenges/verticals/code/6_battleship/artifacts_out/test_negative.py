import pytest
from abstract_class import ShipPlacement, Turn
from pydantic import ValidationError

def test_ship_placement_out_of_bounds(battleship_game):
    # Test if a ship placement out of bounds raises a ValueError with the message "Placement out of bounds"
    game_id = battleship_game.create_game()

    try:
        out_of_bounds_ship = ShipPlacement(
            ship_type="battleship",
            start={"row": 11, "column": "Z"}, # The row and column values are out of bounds
            direction="horizontal",
        )
    except ValidationError:  # Use the directly imported ValidationError class
        pass
    else:
        with pytest.raises(ValueError, match="Placement out of bounds"):
            battleship_game.create_ship_placement(game_id, out_of_bounds_ship)


def test_no_ship_overlap(battleship_game):
    # Test if placing two ships on the same cell raises a ValueError
    game_id = battleship_game.create_game()
    placement1 = ShipPlacement(
        ship_type="battleship", start={"row": 1, "column": "A"}, direction="horizontal"
    )
    battleship_game.create_ship_placement(game_id, placement1)
    placement2 = ShipPlacement(
        ship_type="cruiser", start={"row": 1, "column": "A"}, direction="horizontal" # The cruiser overlaps with the battleship
    )
    with pytest.raises(ValueError):
        battleship_game.create_ship_placement(game_id, placement2)


def test_cant_hit_before_ships_placed(battleship_game):
    # Test if creating a turn before placing all ships raises a ValueError with the message "All ships must be placed before starting turns"
    game_id = battleship_game.create_game()
    placement1 = ShipPlacement(
        ship_type="battleship", start={"row": 1, "column": "A"}, direction="horizontal"
    )
    battleship_game.create_ship_placement(game_id, placement1)
    placement2 = ShipPlacement(
        ship_type="cruiser", start={"row": 4, "column": "D"}, direction="horizontal"
    )
    battleship_game.create_ship_placement(game_id, placement2)
    turn = Turn(target={"row": 1, "column": "A"})
    with pytest.raises(
        ValueError, match="All ships must be placed before starting turns"
    ):
        battleship_game.create_turn(game_id, turn)


def test_cant_place_ship_after_all_ships_placed(battleship_game, initialized_game_id):
    # Test if trying to place a ship after all ships have been placed raises a ValueError with the message "All ships are already placed. Cannot place more ships."
    game = battleship_game.get_game(initialized_game_id)
    additional_ship = ShipPlacement(
        ship_type="carrier", start={"row": 2, "column": "E"}, direction="horizontal"
    )

    with pytest.raises(
        ValueError, match="All ships are already placed. Cannot place more ships."
    ):
        battleship_game.create_ship_placement(initialized_game_id, additional_ship)


def test_ship_placement_invalid_direction(battleship_game):
    # Test if a ship placement with an invalid direction raises a ValueError with the message "Invalid ship direction"
    game_id = battleship_game.create_game()

    with pytest.raises(ValueError, match="Invalid ship direction"):
        invalid_direction_ship = ShipPlacement(
            ship_type="battleship",
            start={"row": 1, "column": "A"},
            direction="diagonal", # The direction is invalid
        )
        battleship_game.create_ship_placement(game_id, invalid_direction_ship)


def test_invalid_ship_type(battleship_game):
    # Test if a ship placement with an invalid ship type raises a ValueError with the message "Invalid ship type"
    game_id = battleship_game.create_game()
    invalid_ship = ShipPlacement(
        ship_type="spacecraft", start={"row": 1, "column": "A"}, direction="horizontal" # The ship type is invalid
    )
    with pytest.raises(ValueError, match="Invalid ship type"):
        battleship_game.create_ship_placement(game_id, invalid_ship)


def test_ship_placement_extends_beyond_boundaries(battleship_game):
    # Test if a ship placement that extends beyond the board boundaries raises a ValueError
    game_id = battleship_game.create_game()

    with pytest.raises(ValueError, match="Ship extends beyond board boundaries"):
        ship_extending_beyond = ShipPlacement(
            ship_type="battleship",
            start={"row": 1, "column": "H"},
            direction="horizontal", # The ship extends beyond the board boundaries
        )
        battleship_game.create_ship_placement(game_id, ship_extending_beyond)

    with pytest.raises(ValueError, match="Ship extends beyond board boundaries"):
        ship_extending_beyond = ShipPlacement(
            ship_type="cruiser", start={"row": 9, "column": "A"}, direction="vertical" # The ship extends beyond the board boundaries
        )
        battleship_game.create_ship_placement(game_id, ship_extending_beyond)
