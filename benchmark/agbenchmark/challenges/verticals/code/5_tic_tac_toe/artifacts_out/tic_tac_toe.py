import pprint


def column(matrix: list, i: int) -> list:
    """Return the i-th column of the matrix."""
    return [row[i] for row in matrix]


def check(lst: list) -> int | None:
    """Check if all elements in the list are the same and not zero.

    Returns the common element if true, otherwise None.
    """
    if len(set(lst)) <= 1 and lst[0] != 0:
        return lst[0]
    return None


def check_diag(board: list, offset: int = 0) -> int | None:
    """Check if the diagonal with the given offset is a win for a player.

    Returns the player number if true, otherwise None.
    """
    if (
        board[offset][offset] == board[1 + offset][1 + offset]
        and board[1 + offset][1 + offset] == board[2 + offset][2 + offset]
    ):
        if board[offset][offset] != 0:
            return board[offset][offset]
    return None


def place_item(row: int, column: int, board: list, current_player: int) -> None:
    """Place the current player's item on the board at the given row and column.

    Does not allow placing an item on an already occupied space.
    """
    if 0 <= row < 3 and 0 <= column < 3 and board[row][column] == 0:
        board[row][column] = current_player
    else:
        raise ValueError("Invalid input")


def swap_players(player: int) -> int:
    """Swap the current player between 1 and 2."""
    if player == 2:
        return 1
    else:
        return 2


def winner(board: list) -> int | None:
    """Check if there is a winner on the board.

    Returns the player number if true, otherwise None.
    """
    for row in board:
        if (result := check(row)) is not None:
            return result
    for column_index in range(len(board[0])):
        if (result := check(column(board, column_index))) is not None:
            return result
    if (result := check_diag(board)) is not None:
        return result
    if (result := check_diag(board, offset=1)) is not None:
        return result
    return None


def get_location() -> tuple[int, int]:
    """Get the location for the next move as a tuple of row and column."""
    while True:
        location = input(
            "Choose where to play. Enter two numbers separated by a comma, for example: 1,1 "
        )
        print(f"\nYou picked {location}")
        try:
            coordinates = [int(x) for x in location.split(",")]
            if len(coordinates) == 2 and all(0 <= x < 3 for x in coordinates):
                return tuple(coordinates)
            else:
                raise ValueError("Invalid input")
        except ValueError as e:
            print(e)


def game_play() -> None:
    """Play a game of tic-tac-toe."""
    num_moves = 0
    pp = pprint.PrettyPrinter(width=20)
    current_player = 1
    board = [[0 for x in range(3)] for x in range(3)]

    while
