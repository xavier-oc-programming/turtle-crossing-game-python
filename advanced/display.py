import sys
import time
from turtle import Screen, Turtle

from config import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    SCREEN_BG,
    SCREEN_TITLE,
    PLAYER_SHAPE,
    PLAYER_HEADING,
    CAR_STRETCH_WID,
    CAR_STRETCH_LEN,
    HUD_X,
    HUD_Y,
    HUD_FONT_SIZE,
    FINISH_LINE_DISPLAY_Y,
    WELCOME_LINE_DELAY,
    LEVEL_UP_FLASH_DURATION,
)


class Display:
    """Owns every turtle object and all rendering.  No game logic lives here."""

    def __init__(self) -> None:
        self.screen: Screen = Screen()
        self.screen.bgcolor(SCREEN_BG)
        self.screen.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
        self.screen.title(SCREEN_TITLE)
        self.screen.tracer(0)

        # Game object turtles
        self._player: Turtle = self._make_player()
        self._car_turtles: list[Turtle] = []   # pool managed per-frame

        # Single writer for ALL text (HUD + overlays)
        self._writer: Turtle = self._make_writer()

        # Static elements drawn once and never cleared
        self._draw_finish_line()

        self.screen.listen()

    # ------------------------------------------------------------------
    # Factory helpers
    # ------------------------------------------------------------------

    def _make_player(self) -> Turtle:
        t = Turtle()
        t.shape(PLAYER_SHAPE)
        t.color("black")
        t.penup()
        t.setheading(PLAYER_HEADING)
        return t

    def _make_writer(self) -> Turtle:
        t = Turtle()
        t.hideturtle()
        t.penup()
        t.color("white")
        return t

    def _make_car(self, color: str) -> Turtle:
        t = Turtle()
        t.shape("square")
        t.color(color)
        t.shapesize(stretch_wid=CAR_STRETCH_WID, stretch_len=CAR_STRETCH_LEN)
        t.penup()
        return t

    def _draw_finish_line(self) -> None:
        """Horizontal finish line — drawn once in __init__, never cleared."""
        line = Turtle()
        line.hideturtle()
        line.penup()
        line.color("white")
        line.goto(-SCREEN_WIDTH // 2, FINISH_LINE_DISPLAY_Y)
        line.pendown()
        line.goto(SCREEN_WIDTH // 2, FINISH_LINE_DISPLAY_Y)

    # ------------------------------------------------------------------
    # Per-frame render calls (called every tick from main)
    # ------------------------------------------------------------------

    def render_player(self, x: float, y: float) -> None:
        self._player.goto(x, y)

    def render_cars(self, cars: list[dict]) -> None:
        """Sync car turtles to the logic list.  Grows the pool as needed."""
        # Grow pool if more cars than turtles
        while len(self._car_turtles) < len(cars):
            self._car_turtles.append(self._make_car("white"))

        for i, car in enumerate(cars):
            t = self._car_turtles[i]
            t.color(str(car["color"]))
            t.goto(float(car["x"]), float(car["y"]))
            t.showturtle()

        # Hide excess turtles
        for i in range(len(cars), len(self._car_turtles)):
            self._car_turtles[i].hideturtle()

    def render_score(self, level: int, high_score: int = 0) -> None:
        self._writer.clear()
        self._writer.color("white")
        self._writer.goto(HUD_X, HUD_Y)
        self._writer.write(
            f"Level: {level}   Best: {high_score}",
            align="left",
            font=("Courier", HUD_FONT_SIZE, "normal"),
        )

    # ------------------------------------------------------------------
    # Welcome / title screen — returns "start" or None (quit)
    # ------------------------------------------------------------------

    def show_welcome(self) -> str | None:
        # Hide game objects while showing the title screen
        self._player.hideturtle()
        for t in self._car_turtles:
            t.hideturtle()

        lines: list[tuple[str, int, str, int]] = [
            # (text, font_size, style, y_position)
            ("TURTLE CROSSING",          36, "bold",   120),
            ("",                          0, "normal",  80),
            ("Cross the road without",   18, "normal",  50),
            ("getting hit by a car!",    18, "normal",  20),
            ("",                          0, "normal",  -5),
            ("Each crossing = +1 level", 14, "normal", -30),
            ("Cars get faster every level", 14, "normal", -55),
            ("",                          0, "normal", -80),
            ("Controls:",                16, "normal", -100),
            ("  \u2191  move up",         15, "normal", -125),
            ("  SPACE  pause",           15, "normal", -150),
            ("",                          0, "normal", -175),
            ("[ SPACE ]  start",         16, "bold",   -200),
            ("[ Q ]  quit",              14, "normal", -225),
        ]

        for text, size, style, y in lines:
            if text:
                self._writer.goto(0, y)
                self._writer.write(text, align="center", font=("Courier", size, style))
            time.sleep(WELCOME_LINE_DELAY)
            self.screen.update()

        _choice: dict[str, str | None] = {"value": None}

        def _on_space() -> None:    _choice["value"] = "start"
        def _on_q() -> None:        _choice["value"] = "quit"

        self.screen.onkeypress(_on_space, "space")
        self.screen.onkeypress(_on_q, "q")
        self.screen.listen()

        while _choice["value"] is None:
            time.sleep(0.05)
            self.screen.update()

        self.screen.onkeypress(None, "space")
        self.screen.onkeypress(None, "q")

        if _choice["value"] == "quit":
            self._writer.clear()
            return None

        self._writer.clear()
        self._player.showturtle()
        return _choice["value"]

    # ------------------------------------------------------------------
    # Pause overlay
    # ------------------------------------------------------------------

    def show_pause(self) -> bool:
        """Overlay PAUSED on the frozen game state.  Do NOT clear screen first.

        Returns True  → resume.
        Returns False → return to title screen.
        """
        self._writer.goto(0, 30)
        self._writer.color("white")
        self._writer.write(
            "PAUSED",
            align="center",
            font=("Courier", 50, "bold"),
        )
        self._writer.goto(0, -30)
        self._writer.write(
            "[ SPACE ]  resume        [ R ]  return to title screen",
            align="center",
            font=("Courier", 16, "normal"),
        )
        self.screen.update()

        _choice: dict[str, bool | None] = {"value": None}

        def _on_space() -> None:    _choice["value"] = True
        def _on_r() -> None:        _choice["value"] = False

        self.screen.onkeypress(_on_space, "space")
        self.screen.onkeypress(_on_r, "r")
        self.screen.listen()

        while _choice["value"] is None:
            time.sleep(0.05)
            self.screen.update()

        self._writer.clear()
        self.screen.onkeypress(None, "space")
        self.screen.onkeypress(None, "r")

        return bool(_choice["value"])

    # ------------------------------------------------------------------
    # Game-over overlay
    # ------------------------------------------------------------------

    def show_game_over(self, level: int, high_score: int, new_high: bool) -> bool:
        """Overlay GAME OVER on the frozen game state.  Do NOT clear screen first.

        Returns True  → play again.
        Returns False → return to title screen.
        """
        self._writer.goto(0, 60)
        self._writer.color("red")
        self._writer.write(
            "GAME OVER",
            align="center",
            font=("Courier", 50, "bold"),
        )
        self._writer.goto(0, 0)
        self._writer.color("white")
        record_text = "  NEW RECORD!" if new_high else ""
        self._writer.write(
            f"Level reached: {level}{record_text}",
            align="center",
            font=("Courier", 20, "normal"),
        )
        self._writer.goto(0, -40)
        self._writer.write(
            f"Best: {high_score}",
            align="center",
            font=("Courier", 16, "normal"),
        )
        self._writer.goto(0, -80)
        self._writer.write(
            "[ SPACE ]  play again        [ R ]  return to title screen",
            align="center",
            font=("Courier", 16, "normal"),
        )
        self.screen.update()

        _choice: dict[str, bool | None] = {"value": None}

        def _on_space() -> None:    _choice["value"] = True
        def _on_r() -> None:        _choice["value"] = False

        self.screen.onkeypress(_on_space, "space")
        self.screen.onkeypress(_on_r, "r")
        self.screen.listen()

        while _choice["value"] is None:
            time.sleep(0.05)
            self.screen.update()

        self._writer.clear()
        self.screen.onkeypress(None, "space")
        self.screen.onkeypress(None, "r")

        return bool(_choice["value"])

    # ------------------------------------------------------------------
    # Level-up flash
    # ------------------------------------------------------------------

    def show_level_up(self, level: int) -> None:
        """Brief centred flash showing the new level number."""
        self._writer.goto(0, 0)
        self._writer.color("yellow")
        self._writer.write(
            f"LEVEL {level}",
            align="center",
            font=("Courier", 40, "bold"),
        )
        self.screen.update()
        time.sleep(LEVEL_UP_FLASH_DURATION)
        self._writer.clear()

    # ------------------------------------------------------------------
    # Teardown
    # ------------------------------------------------------------------

    def close(self) -> None:
        # NEVER use screen.bye() — it triggers tkinter cleanup that raises
        # turtle.Terminator or TclError, leaving the subprocess broken.
        # sys.exit(0) terminates cleanly; subprocess.run() in menu.py
        # receives exit code 0 and the terminal menu reappears normally.
        sys.exit(0)
