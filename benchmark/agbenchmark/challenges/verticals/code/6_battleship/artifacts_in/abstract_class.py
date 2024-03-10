from typing import Any, Callable, List, TypeVar, Union
from pydantic import BaseModel, Field, ValidationError
from pydantic.json import pydantic_encoder
from typing_extensions import overload


from abc import ABC, abstractmethod
from typing import Any, Callable, List, TypeVar, Union

from pydantic import BaseModel, Field, ValidationError, validator
from pydantic.json import pydantic_encoder
from typing_extensions import overload

T = TypeVar("T")


class ShipPlacement(BaseModel):
    ship_type: str
    start: dict = Field(default_factory=lambda: {"row": 0, "column": "A"})  # {"row": int, "column": str}
    direction: str

    @validator("start")
    def validate_start(cls, start):
        row, column = start.get("row"), start.get("column")

        if not (1 <= row <= 10):
            raise ValueError("Row must be between 1 and 10 inclusive.")

        if column not in list("ABCDEFGHIJ"):
            raise ValueError("Column must be one of A, B, C, D, E, F, G, H, I, J.")

        return start


class Turn(BaseModel):
    target: dict = Field(default_factory=lambda: {"row": 0, "column": "A"})  # {"row": int, "column": str}


class TurnResponse(BaseModel):
    result: str
    ship_type: Optional[str] = None  # This would be None if the result is a miss


class GameStatus(BaseModel):
    is_game_over: bool
    winner: Optional[str]


class Game(BaseModel):
    game_id: str
    players: List[str]
    board: dict = {}  # This could represent the state of the game board, you might need to flesh this out further
    ships: List[ShipPlacement] = []  # List of ship placements for this game
    turns: List[Turn] = []  # List of turns that have been taken

    def __getitem__(self, item: str) -> Any:
        return getattr(self, item)

    def __setitem__(self, key: str, value: Any) -> None:
        setattr(self, key, value)

    @overload
    @classmethod
    def create_ship_placement(cls, game_id: str, placement: ShipPlacement) -> None:
        ...

    @overload
    @classmethod
    def create_ship_placement(cls, game_id: str, placement: dict) -> None:
        ...

    @classmethod
    def create_ship_placement(cls, game_id: str, placement: Union[ShipPlacement, dict]) -> None:
        if isinstance(placement, dict):
            placement = ShipPlacement(**placement)
        # Place a ship on the grid

    @overload
    @classmethod
    def create_turn(cls, game_id: str, turn: Turn) -> TurnResponse:
        ...

    @overload
    @classmethod
    def create_turn(cls, game_id: str, turn: dict) -> TurnResponse:
        ...

    @classmethod
    def create_turn(cls, game_id: str, turn: Union[Turn, dict]) -> TurnResponse:
        if isinstance(turn, dict):
            turn = Turn
