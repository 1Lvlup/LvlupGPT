from abc import ABC, abstractmethod
from typing import (
    Any,
    ClassVar,
    Dict,
    Final,
    List,
    Optional,
    Type,
    TypeVar,
    Union,
)

from pydantic import BaseModel, validator

T = TypeVar("T")


class ShipPlacement(BaseModel):
    ship_type: str
    start: Dict[str, int]  # {"row": int, "column": int}
    direction: str

    @validator("start")
    def validate_start(cls, start):
        row, column = start.get("row"), start.get("column")

        if not (1 <= row <= 10):
            raise ValueError("Row must be between 1 and 10 inclusive.")

        if not (1 <= column <= 10):
            raise ValueError("Column must be between 1 and 10 inclusive.")

        return start


class Turn(BaseModel):
    target: Dict[str, int]  # {"row": int, "column": int}


class TurnResponse(BaseModel):
    result: str
    ship_type: Optional[str]


class GameStatus(BaseModel):
    is_game_over: bool
    winner: Optional[str]


class Game(BaseModel):
    game_id: str
    players: List[str]
    board: Dict[str, str]  # This could represent the state of the game board, you might need to flesh this out further
    ships: List[ShipPlacement]
    turns: List[Turn]


class AbstractBattleship(ABC):
    SHIP_LENGTHS: ClassVar[Final[Dict[str, int]]] = {
        "carrier": 5,
        "battleship": 4,
        "cruiser": 3,
        "submarine": 3,
        "destroyer": 2,
    }

    def __init_subclass__(cls, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)

        for method_name in (
            "create_ship_placement",
            "create_turn",
            "get_game_status",
            "get_winner",
            "get_game",
            "delete_game",
            "create_game",
        ):
            method = getattr(cls, method_name, None)
            if not isinstance(method, (classmethod, abstractmethod)):
                raise NotImplementedError(f"{method_name} must be implemented.")

    @abstractmethod
    def create_ship_placement(self, game_id: str, placement: ShipPlacement) -> None:
        pass

    @abstractmethod
    def create_turn(self, game_id: str, turn: Turn) -> TurnResponse:
        pass

    @property
    @abstractmethod
    def game_status(self) -> GameStatus:
        pass

    @abstractmethod
    def get_winner(self, game_id: str) -> str:
        pass

    @property
    @abstractmethod
    def game(self) -> Game:
        pass

    @abstractmethod
    def delete_game(self, game_id: str) -> None:
        pass

    @classmethod
    @abstractmethod
    def create_game(cls: Type[T], *args: Any, **kwargs: Any) -> T:
        pass

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}
