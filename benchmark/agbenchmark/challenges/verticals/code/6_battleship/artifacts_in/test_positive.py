from abstract_class import ShipPlacement, Turn

def test_turns_and_results(battleship_game, initialized_game_id):
    turn = Turn(target={"row": 1, "column": "A"})
    response = battleship_game.create_turn(initialized_game_id, turn)

    if response.result == "hit":
        assert response.ship_type == "carrier"
    
    game = battleship_game.get_game(initialized_game_id)
    assert turn in game.turns

