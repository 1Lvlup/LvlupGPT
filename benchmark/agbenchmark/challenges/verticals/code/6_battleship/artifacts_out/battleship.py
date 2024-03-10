from typing import Dict, NamedTuple, Optional

from abstract_class import (AbstractBattleship, Game, GameStatus,
                            ShipPlacement, Turn, TurnResponse)

class ShipPosition(NamedTuple):
    row: int
    col: int

class Battleship(AbstractBattleship):
    def __init__(self):
        self.games: Dict[str, Game] = {}
        self.SHIP_LENGTHS = {
            "carrier": 5,
            "battleship": 4,
            "cruiser": 3,
            "submarine": 3,
            "destroyer": 2,
        }

    def create_game(self) -> str:
        game_id = str(len(self.games))
        new_game = Game(
            game_id=game_id,
            players=[],
            board={},
            ships=[],
            turns=[],
        )

        self.games[game_id] = new_game
        return new_game.game_id

    def create_ship_placement(self, game_id: str, placement: ShipPlacement) -> None:
        game = self.games.get(game_id)

        if not game:
            raise ValueError(f"Game with ID {game_id} not found.")

        if placement.direction not in ["horizontal", "vertical"]:
            raise ValueError("Invalid ship direction")

        if self.all_ships_placed(game):
            raise ValueError("All ships are already placed. Cannot place more ships.")

        ship_length = self.SHIP_LENGTHS.get(placement.ship_type)
        if not ship_length:
            raise ValueError(f"Invalid ship type {placement.ship_type}")

        start_pos = ShipPosition(*placement.start)

        if not self.is_valid_placement(game, start_pos, ship_length, placement.direction):
            raise ValueError("Placement out of bounds or overlapping with another ship")

        self.place_ship(game, start_pos, ship_length, placement.direction, placement.ship_type)

    def create_turn(self, game_id: str, turn: Turn) -> TurnResponse:
        game = self.games.get(game_id)

        if not game:
            raise ValueError(f"Game with ID {game_id} not found.")

        if not self.all_ships_placed(game):
            raise ValueError("All ships must be placed before starting turns")

        target_pos = ShipPosition(int(turn.target["row"]), ord(turn.target["column"]) - ord("A"))
        hit_ship = game.board.get(target_pos)

        game.turns.append(turn)

        if hit_ship == "hit":
            return TurnResponse(result="miss", ship_type=None)

        if hit_ship:
            ship_placement = next(sp for sp in game.ships if sp.ship_type == hit_ship)
            self.mark_ship_hit(game, target_pos, ship_placement)

            if self.is_ship_sunk(game, ship_placement):
                return TurnResponse(result="sunk", ship_type=hit_ship)

        return TurnResponse(result="hit", ship_type=hit_ship)

    def get_game_status(self, game_id: str) -> GameStatus:
        game = self.games.get(game_id)

        if not game:
            raise ValueError(f"Game with ID {game_id} not found.")

        hits = sum(1 for _, status in game.board.items() if status == "hit")

        total_ships_length = sum(
            self.SHIP_LENGTHS[ship.ship_type] for ship in game.ships
        )

        if hits == total_ships_length:
            return GameStatus(is_game_over=True, winner="player")
        else:
            return GameStatus(is_game_over=False, winner=None)

    def get_winner(self, game_id: str) -> Optional[str]:
        game_status = self.get_game_status(game_id)

        if game_status.is_game_over:
            return game_status.winner
        else:
            return None

    def get_game(self, game_id: str) -> Optional[Game]:
        return self.games.get(game_id)

    def delete_game(self, game_id: str) -> None:
        if game_id in self.games:
            del self.games[game_id]

    def all_ships_placed(self, game: Game) -> bool:
        placed_ship_types = set([placement.ship_type for placement in game.ships])
        return placed_ship_types == set(self.SHIP_LENGTHS.keys())

    def is_valid_placement(self, game: Game, start_pos: ShipPosition, length: int, direction: str) -> bool:
        if direction == "horizontal":
            return (start_pos.col + length - 1) <= 10 and all(
                (row, col) not in game.board for row, col in zip(range(start_pos.row, start_pos.row + length), range(start_pos.col, start_pos.col + length))
            )
        else:
            return (start_pos.row + length - 1) <= 10 and all(
                (row, col) not in game.board for row, col in zip(range(start_pos.row, start_pos.row + length), range(start_pos.col, start_pos.col + length))
            )

    def place_ship(self, game: Game, start_pos: ShipPosition, length: int, direction: str, ship_type: str) -> None:
        if direction == "horizontal":
            for col in range(start_pos.col, start_pos.col + length):
                game.board[(start_pos.row, col)] = ship_type
                game
