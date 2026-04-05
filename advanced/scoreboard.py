from pathlib import Path
from config import STARTING_LEVEL

DATA_FILE = Path(__file__).parent / "data.txt"


class Scoreboard:
    """Pure logic: tracks current level and persists the high score.  No turtle, no UI."""

    def __init__(self) -> None:
        self.level: int = STARTING_LEVEL
        self.high_score: int = self._load_high_score()

    def _load_high_score(self) -> int:
        try:
            return int(DATA_FILE.read_text().strip())
        except (FileNotFoundError, ValueError):
            return 0

    def increment_level(self) -> None:
        self.level += 1

    def reset(self) -> None:
        self.level = STARTING_LEVEL

    def is_new_high_score(self) -> bool:
        return self.level > self.high_score

    def save_high_score(self) -> None:
        if self.is_new_high_score():
            self.high_score = self.level
            DATA_FILE.write_text(str(self.high_score))
