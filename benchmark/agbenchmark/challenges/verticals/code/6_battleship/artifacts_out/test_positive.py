import abc
import random
from typing import Any, Dict, Optional

import pytest

from abstract_class import ShipPlacement, Turn


@pytest.fixture
def battleship_game(request):
    return request.getfixturevalue("battleship_game")


@pytest.fixture
def initialized_game_id(battleship_game):
    game_id = battleship_game.create_game()
    return game_id


def test_turns_and_results(battleship_game, initialized_game_id):
    turn = Turn(target={"row": 1, "column": "A"})
    response = battleship_game.create_turn(initialized_game_id, turn)

    assert response.result in ["hit", "miss"], f"Expected result to be 'hit' or 'miss', but got {response.result}"
    if response.result == "hit":
        assert response.ship_type == "carrier", f"Expected ship_type to be 'carrier', but got {response.ship_type}"
    game = battleship_game.get_game(initialized_game_id)
    assert turn in game.turns, f"Expected turn to be in game.turns, but it's not."


def test_game_status_and_winner(battleship_game):
    game_id = battleship_game.create_game()
    status = battleship_game.get_game_status(game_id)
    assert isinstance(status.is_game_over, bool), f"Expected is_game_over to be a boolean, but got {type(status.is_game_over)}"
    if status.is_game_over:
        winner = battleship_game.get_winner(game_id)
        assert winner is not None, f"Expected winner to be set, but it's None."


def test_delete_game(battleship_game):
    game_id = battleship_game.create_game()
    battleship_game.delete_game(game_id)
    game = battleship_game.get_game(game_id)
    assert game is None, f"Expected game to be None, but it's not."


def test_ship_rotation(battleship_game):
    game_id = battleship_game.create_game()
    placement_horizontal = ShipPlacement(
        ship_type="battleship", start={"row": 1, "column": "B"}, direction="horizontal"
    )
    battleship_game.create_ship_placement(game_id, placement_horizontal)
    placement_vertical = ShipPlacement(
        ship_type="cruiser", start={"row": 3, "column": "D"}, direction="vertical"
    )
    battleship_game.create_ship_placement(game_id, placement_vertical)
    game = battleship_game.get_game(game_id)
    assert placement_horizontal in game.ships, f"Expected placement_horizontal to be in game.ships, but it's not."
    assert placement_vertical in game.ships, f"Expected placement_vertical to be in game.ships, but it's not."


def test_game_state_updates(battleship_game, initialized_game_id):
    target_row, target_column = 3, random.choice("ABCDEFGHIJ")
    turn = Turn(target={"row": target_row, "column": target_column})
    battleship_game.create_turn(initialized_game_id, turn)

    game = battleship_game.get_game(initialized_game_id)

    target_key = (target_row, ord(target_column) - ord("A"))
    assert target_key in game.board, f"Expected target_key to be in game.board, but it's not."
    assert game.board[target_key] in ["hit", "miss"], f"Expected 'hit' or 'miss', but got {game.board[target_key]}."


def test_ship_sinking_feedback(battleship_game, initialized_game_id):
    hits = ["A", "B", "C", "D"]
    static_moves = [
        {"row": 1, "column": "E"},
        {"row": 1, "column": "F"},
        {"row": 1, "column": "G"},
        {"row": 1, "column": "H"},
    ]

    for index, hit in enumerate(hits):
        turn = Turn(target={"row": 2, "column": hit})
        response = battleship_game.create_turn(initialized_game_id, turn)
        assert response.ship_type == "battleship", f"Expected ship_type to be 'battleship', but got {response.ship_type}"

        static_turn = Turn(target=static_moves[index])
        battleship_game.create_turn(initialized_game_id, static_turn)

    assert response.result == "sunk", f"Expected 'sunk', but got {response.result}."


def test_restart_game(battleship_game):
    game_id = battleship_game.create_game()
    battleship_game.delete_game(game_id)
    game_id = battleship_game.create_game()  # Use the returned game_id after recreating the game
    game = battleship_game.get_game(game_id)
    assert game is not None, f"Expected game to be not None, but it's None."


def test_ship_edge_overlapping(battleship
