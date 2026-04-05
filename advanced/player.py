from config import (
    PLAYER_START_X,
    PLAYER_START_Y,
    PLAYER_MOVE_DISTANCE,
    FINISH_LINE_Y,
)


class Player:
    """Pure logic: tracks the player's x/y position.  No turtle, no UI."""

    def __init__(self) -> None:
        self.x: float = float(PLAYER_START_X)
        self.y: float = float(PLAYER_START_Y)

    def move_up(self) -> None:
        self.y += PLAYER_MOVE_DISTANCE

    def reset_to_start(self) -> None:
        self.x = float(PLAYER_START_X)
        self.y = float(PLAYER_START_Y)

    def has_crossed(self) -> bool:
        return self.y >= FINISH_LINE_Y
