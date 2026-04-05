# ---------------------------------------------------------------------------
# Screen
# ---------------------------------------------------------------------------
SCREEN_WIDTH: int = 600
SCREEN_HEIGHT: int = 600
SCREEN_BG: str = "white"
SCREEN_TITLE: str = "Turtle Crossing"

# ---------------------------------------------------------------------------
# Player
# ---------------------------------------------------------------------------
PLAYER_SHAPE: str = "turtle"
PLAYER_START_X: int = 0
PLAYER_START_Y: int = -260
PLAYER_HEADING: int = 90          # faces upward
PLAYER_MOVE_DISTANCE: int = 15    # pixels per Up key press
FINISH_LINE_Y: int = 280          # y-threshold that counts as a crossing

# ---------------------------------------------------------------------------
# Cars
# ---------------------------------------------------------------------------
CAR_COLORS: list[str] = ["red", "orange", "yellow", "green", "blue", "purple"]
CAR_STRETCH_WID: int = 1
CAR_STRETCH_LEN: int = 2
CAR_SPAWN_X: int = 300            # cars spawn at the right edge
CAR_DESPAWN_X: int = -320         # cars are removed once they pass the left edge
CAR_Y_MIN: int = -250             # lowest possible spawn y
CAR_Y_MAX: int = 250              # highest possible spawn y
CAR_SPAWN_CHANCE: int = 6         # 1-in-N chance to spawn a car each tick
STARTING_CAR_SPEED: float = 2.5   # pixels per tick at level 1
SPEED_INCREMENT: float = 2.4      # added to car_speed on each level up

# ---------------------------------------------------------------------------
# Collision detection
# ---------------------------------------------------------------------------
COLLISION_WIDTH_MARGIN: int = 25  # half-width hit zone
COLLISION_HEIGHT_MARGIN: int = 30 # half-height hit zone

# ---------------------------------------------------------------------------
# Scoring / levels
# ---------------------------------------------------------------------------
STARTING_LEVEL: int = 1

# ---------------------------------------------------------------------------
# Display timings
# ---------------------------------------------------------------------------
GAME_TICK: float = 0.032          # ~60 FPS (seconds per tick)
WELCOME_LINE_DELAY: float = 0.06  # seconds between each title-screen line reveal
LEVEL_UP_FLASH_DURATION: float = 0.8  # seconds the "LEVEL X" flash stays visible

# ---------------------------------------------------------------------------
# HUD / layout
# ---------------------------------------------------------------------------
HUD_Y: int = 260                  # y-position of the level counter
HUD_X: int = -270                 # x-position of the level counter (left-aligned)
HUD_FONT_SIZE: int = 24
FINISH_LINE_DISPLAY_Y: int = 270  # y of the visual finish line drawn on screen
ROAD_TOP_Y: int = 250             # top boundary of the road area (car spawns)
ROAD_BOTTOM_Y: int = -250         # bottom boundary of the road area
