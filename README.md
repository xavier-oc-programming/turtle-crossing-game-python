# Turtle Crossing Game — Python

100 Days of Code · Day 23 · Frogger-style crossing game in two versions: original course build and a full OOP/architecture rebuild.

---

## 1. Quick Start

```bash
# Clone
git clone https://github.com/xavier-oc-programming/turtle-crossing-game-python.git
cd turtle-crossing-game-python

# Launch the menu (Python 3.10+)
python menu.py
```

From the menu:
- `1` — Original course build
- `2` — Advanced OOP rebuild (pause, title screen, high score)
- `q` — Exit

No third-party packages. `turtle` and `tkinter` are bundled with CPython.

---

## 2. Builds Comparison

| Feature | Original | Advanced |
|---|---|---|
| Screen size | 600 × 600 | 600 × 600 |
| Player movement | Up arrow | Up arrow (smooth hold) |
| Car spawning | Random, 1-in-6 per tick | Random, 1-in-6 per tick |
| Collision detection | Margin-based | Margin-based |
| Level display | Top-left HUD | Top-left HUD + best score |
| Level-up flash | None | "LEVEL X" centred flash |
| High score persistence | None | `data.txt` (survives restarts) |
| Title screen | None | Animated reveal with controls |
| Pause | None | Space — overlay on frozen game |
| Game over | "GAME OVER" text, click to close | Overlay — Space / R options |
| Return to title | No (window closes) | R — same window, no restart |
| Menu launcher | No | Yes (`menu.py`) |
| Architecture | Procedural + OOP mixed | Pure-logic + display separation |

---

## 3. Controls

### Title screen
| Key | Action |
|---|---|
| Space | Start game |
| Q | Quit (closes window, returns to terminal menu) |

### Gameplay
| Key | Action |
|---|---|
| ↑ (Up arrow) | Move turtle up (hold for continuous movement) |
| Space | Pause |

### Pause overlay
| Key | Action |
|---|---|
| Space | Resume |
| R | Return to title screen |

### Game over overlay
| Key | Action |
|---|---|
| Space | Play again |
| R | Return to title screen |

---

## 4. Gameplay Rules

1. The turtle starts at the bottom centre of the screen.
2. Press Up (hold for smooth movement) to move toward the finish line.
3. Cars spawn from the right edge at random y-positions and drive left.
4. If a car overlaps the turtle — collision — the game ends.
5. Reaching y ≥ 280 (the finish line) counts as a successful crossing.
6. On each crossing: level increments, car speed increases, turtle resets to start.
7. The game has no upper level limit — it ends only on collision.
8. The best level reached is saved to `advanced/data.txt` and shown in the HUD.

---

## 5. Features

### Both builds

**Random car spawning**
Each tick has a 1-in-6 chance of spawning a new car at `x = 300` and a random y-position between −240 and 240. Cars are coloured randomly from six options.

**Margin-based collision detection**
The hit zone is ±25 px horizontally and ±30 px vertically around the player's position, matching the turtle head and car body dimensions.

**Progressive difficulty**
Every successful crossing adds 2.4 to the car speed. Cars that started visibly slow become dangerously fast within a few levels.

### Advanced only

**Animated title screen**
Lines are revealed one by one with a short delay between each, giving the screen a typewriter feel. All game objects are hidden during the title; they reappear when Space is pressed.

**Pause overlay**
Space pauses the game mid-tick. The overlay is drawn on top of the frozen game state — the screen is not cleared. Space is unregistered before entering the overlay so it cannot re-trigger the pause handler from inside the overlay. It is re-registered (with `screen.listen()`) on return.

**Game over overlay**
Instead of closing the window, a "GAME OVER" overlay appears on the frozen state showing the level reached and the best score. Space replays from level 1; R returns to the title screen.

**Level-up flash**
A large yellow "LEVEL X" message flashes centred on screen for 0.8 s after each crossing, then clears. The HUD is redrawn immediately after.

**Persistent high score**
The best level reached is written to `advanced/data.txt` as a plain integer. It is loaded at startup and shown alongside the current level in the HUD throughout the session.

**R never closes the window**
Pressing R from any overlay breaks the inner game loop and returns to the outer loop, which reruns the title screen in the same window. The window only closes when Q is pressed on the title screen (`display.close()` → `sys.exit(0)`).

**`menu.py` launcher**
A terminal menu lets you choose between the two builds or quit. The menu uses `subprocess.run()` with `cwd=` set to the target directory so relative imports inside each build resolve correctly. The menu reappears automatically when the game window closes.

---

## 6. Navigation Flow

### Terminal menu

```
python menu.py
│
├── 1 ──► original/main.py  (subprocess, cwd=original/)
│          └── window closes on click ──► menu reappears
│
├── 2 ──► advanced/main.py  (subprocess, cwd=advanced/)
│          └── sys.exit(0) on Q ──────── menu reappears
│
└── q ──► break ──► terminal exits
```

### In-window state (advanced build)

```
┌─────────────────────────┐
│       TITLE SCREEN      │
│  lines reveal one by one│
│                         │
│  [ SPACE ] start        │
│  [ Q ]     quit         │
└─────────────────────────┘
     │ Space                  │ Q
     ▼                        ▼
┌─────────────────┐      display.close()
│   GAME LOOP     │      sys.exit(0)
│  (inner loop)   │
│                 │
│  ↑  move up     │
│  Space  pause   │
└─────────────────┘
     │                   │                    │
     │ Space             │ car hit            │ crossed
     ▼                   ▼                    ▼
┌───────────┐     ┌──────────────┐    level++, speed++
│  PAUSED   │     │  GAME OVER   │    show_level_up()
│           │     │              │    reset to start
│  Space ──►│     │  Space ─────►│    continue loop
│  resume   │     │  play again  │
│           │     │              │
│  R ───────┤     │  R ──────────┤
└───────────┘     └──────────────┘
     │ R                  │ R
     └──────────┬─────────┘
                ▼
        break inner loop
                │
                ▼
        outer loop repeats
                │
                ▼
        TITLE SCREEN (same window)
```

> **Note:** R never closes the window. The same `Display` instance (and its tkinter window) persists for the entire session. `sys.exit(0)` is the only path that closes it.

---

## 7. Architecture

```
turtle-crossing-game-python/
│
├── menu.py              # Terminal launcher — prints LOGO, loops subprocess.run()
├── art.py               # LOGO constant (ASCII art)
├── requirements.txt     # stdlib only, Python 3.10+ note
├── .gitignore
│
├── docs/
│   └── COURSE_NOTES.md  # Original exercise description and OOP concepts
│
├── original/            # Course files — verbatim, no logic changes
│   ├── main.py          # Screen setup, game loop, collision, level-up
│   ├── player.py        # Player(Turtle) — move_up, reset_position
│   ├── car_manager.py   # CarManager — create_car, move_cars, level_up
│   └── scoreboard.py    # Scoreboard(Turtle) — update, increase_level, game_over
│
└── advanced/            # Full OOP rebuild — logic and display separated
    ├── config.py        # Every constant — zero magic numbers elsewhere
    ├── player.py        # Player — pure logic, x/y only, no turtle
    ├── car_manager.py   # CarManager — pure logic, list of dicts
    ├── scoreboard.py    # Scoreboard — pure logic, high score I/O
    ├── display.py       # Display — owns ALL turtle objects and overlays
    ├── main.py          # Orchestrator — two nested loops, key bindings
    └── data.txt         # Persisted high score (plain integer)
```

---

## 8. Module Reference

### `advanced/player.py` — `class Player`

| Method | Description |
|---|---|
| `__init__()` | Sets `x`, `y` to start position from config |
| `move_up()` | Increments `y` by `PLAYER_MOVE_DISTANCE` |
| `reset_to_start()` | Returns `x`, `y` to `PLAYER_START_X`, `PLAYER_START_Y` |
| `has_crossed() → bool` | Returns `True` if `y >= FINISH_LINE_Y` |

### `advanced/car_manager.py` — `class CarManager`

| Method | Description |
|---|---|
| `__init__()` | Initialises empty `cars` list and `car_speed` from config |
| `create_car()` | 1-in-6 chance to append a new car dict to `self.cars` |
| `move_cars()` | Decrements each car's `x` by `car_speed`; removes off-screen cars |
| `increase_speed()` | Adds `SPEED_INCREMENT` to `car_speed` |
| `detect_collision(player_x, player_y) → bool` | Returns `True` if any car overlaps the player hit zone |
| `reset()` | Clears `cars` list and resets `car_speed` to `STARTING_CAR_SPEED` |

### `advanced/scoreboard.py` — `class Scoreboard`

| Method | Description |
|---|---|
| `__init__()` | Sets `level` to `STARTING_LEVEL`, loads `high_score` from `data.txt` |
| `increment_level()` | Increments `self.level` by 1 |
| `reset()` | Resets `self.level` to `STARTING_LEVEL` |
| `is_new_high_score() → bool` | Returns `True` if current level exceeds saved high score |
| `save_high_score()` | Writes `self.level` to `data.txt` if it is a new high score |

### `advanced/display.py` — `class Display`

| Method | Description |
|---|---|
| `__init__()` | Creates Screen, player turtle, writer turtle; draws finish line |
| `render_player(x, y)` | Moves player turtle to given coordinates |
| `render_cars(cars)` | Syncs car turtle pool to the logic car list |
| `render_score(level, high_score)` | Clears `_writer` and redraws HUD |
| `show_welcome() → str \| None` | Animated title screen; returns `"start"` or `None` (quit) |
| `show_pause() → bool` | Pause overlay; returns `True` (resume) or `False` (title) |
| `show_game_over(level, high_score, new_high) → bool` | Game over overlay; returns `True` (play again) or `False` (title) |
| `show_level_up(level)` | Centred "LEVEL X" flash for `LEVEL_UP_FLASH_DURATION` seconds |
| `close()` | Calls `sys.exit(0)` — the only correct shutdown path |

---

## 9. Configuration Reference

All constants live in `advanced/config.py`. Zero magic numbers exist anywhere else.

| Constant | Default | Description |
|---|---|---|
| `SCREEN_WIDTH` | `600` | Window width in pixels |
| `SCREEN_HEIGHT` | `600` | Window height in pixels |
| `SCREEN_BG` | `"black"` | Background colour |
| `SCREEN_TITLE` | `"Turtle Crossing"` | Window title bar text |
| `PLAYER_SHAPE` | `"turtle"` | Turtle shape name |
| `PLAYER_START_X` | `0` | Player starting x-coordinate |
| `PLAYER_START_Y` | `-260` | Player starting y-coordinate |
| `PLAYER_HEADING` | `90` | Player heading in degrees (upward) |
| `PLAYER_MOVE_DISTANCE` | `15` | Pixels moved per Up key press |
| `FINISH_LINE_Y` | `280` | y-threshold that counts as a crossing |
| `CAR_COLORS` | 6-colour list | Possible car colours |
| `CAR_STRETCH_WID` | `1` | Car turtle shapesize stretch_wid |
| `CAR_STRETCH_LEN` | `2` | Car turtle shapesize stretch_len (2× wide) |
| `CAR_SPAWN_X` | `300` | x where new cars appear |
| `CAR_DESPAWN_X` | `-320` | x past which cars are removed |
| `CAR_Y_MIN` | `-240` | Lowest y for car spawns |
| `CAR_Y_MAX` | `240` | Highest y for car spawns |
| `CAR_SPAWN_CHANCE` | `6` | 1-in-N chance to spawn per tick |
| `STARTING_CAR_SPEED` | `2.5` | Pixels per tick at level 1 |
| `SPEED_INCREMENT` | `2.4` | Speed added per level up |
| `COLLISION_WIDTH_MARGIN` | `25` | Half-width of player hit zone |
| `COLLISION_HEIGHT_MARGIN` | `30` | Half-height of player hit zone |
| `STARTING_LEVEL` | `1` | Level counter initial value |
| `GAME_TICK` | `0.032` | Seconds per tick (~60 FPS) |
| `WELCOME_LINE_DELAY` | `0.06` | Seconds between title-screen line reveals |
| `LEVEL_UP_FLASH_DURATION` | `0.8` | Seconds the level-up flash is visible |
| `HUD_Y` | `260` | y of the level/best score HUD |
| `HUD_X` | `-270` | x of the HUD (left-aligned) |
| `HUD_FONT_SIZE` | `24` | HUD font size |
| `FINISH_LINE_DISPLAY_Y` | `270` | y of the visual finish line |
| `ROAD_TOP_Y` | `250` | Top of the car spawn zone |
| `ROAD_BOTTOM_Y` | `-250` | Bottom of the car spawn zone |

---

## 10. Display Layout

```
y = +300 ─────────────────────────────────────────────────────
           Level: 3   Best: 5          (HUD, white text)
y = +270 ══════════════════════════════════════════════════════  ← finish line (white)
y = +250
           [ cars move right-to-left across this zone ]
           [ random y between -240 and +240           ]
           [ spawned at x=300, despawned at x=-320    ]
y =    0   ·  ·  ·  ·  ·  ·  · (centre)
           
y = -260   🐢  (player start, x=0)

y = -300 ─────────────────────────────────────────────────────

x:  -300                    0                    +300
```

Overlays (PAUSED / GAME OVER) are drawn centred at approximately:
- Heading: `y = +30` to `y = +60` (large bold text)
- Subtext / options: `y = −30` to `y = −80`

---

## 11. Design Decisions

### `sys.exit(0)` instead of `screen.bye()`

`screen.bye()` triggers tkinter's internal cleanup sequence, which can raise `turtle.Terminator` or `TclError` depending on Python version and timing. This leaves the subprocess in an error state, and `subprocess.run()` in `menu.py` may print a traceback or hang. `sys.exit(0)` terminates the process cleanly with exit code 0; `subprocess.run()` returns and the terminal menu reappears normally.

### Two nested loops instead of a state machine

The outer loop handles the title → game → title cycle. The inner loop is the live game tick. This maps directly onto the runtime flow: `break` from the inner loop always means "return to title", which is exactly what R does in every overlay. A state machine would need an explicit `current_state` variable and dispatch logic; the nested loops make the same intent read as plain control flow.

### Space unregistration before every overlay

`onkeypress` binds a handler to a key. If Space is still bound to `trigger_pause` when `show_pause()` is entered, a queued Space event (e.g. the same keypress that triggered the pause) can fire the handler again from *inside* the overlay, immediately setting `keys["pause"] = True` for the next tick. Unregistering Space with `onkeypress(None, "space")` before calling any overlay blocks this. Re-registering after the overlay returns restores normal behaviour.

### `onkeypress` not `onkey` for overlay keys

`onkey` in turtle is an alias for `onkeyrelease`. If you mix `onkeypress` and `onkeyrelease` on the same key you get two independent bindings that can both fire in the same keypress event. All overlay keys use `onkeypress` exclusively to avoid this.

### Movement with `onkeypress` + `onkeyrelease` (flag pattern)

Binding `player.move_up()` directly to `onkey` (as in the original) fires once per OS key-repeat event — movement feels choppy at high tick rates. The advanced build sets a boolean flag on press and clears it on release; the game loop calls `move_up()` every tick while the flag is set. This gives smooth, continuous movement at the full tick rate with no dependency on OS key-repeat settings.

### UI-free logic modules

`player.py`, `car_manager.py`, and `scoreboard.py` import nothing from `turtle` or `tkinter`. This means they can be unit-tested in a headless environment, reasoned about without knowing the rendering layer, and swapped to a different renderer (pygame, tkinter Canvas) without touching the logic. `display.py` is the only file that knows about `turtle`; `main.py` is the only file that knows about both.

### Single `_writer` turtle for all text

One turtle handles all text output: HUD scores, overlay messages, and the title screen. `_writer.clear()` wipes *everything* written by that turtle. This is intentional — it means overlays can be dismissed with one call. The pattern is: every overlay and `show_welcome()` calls `_writer.clear()` at the end; the caller is then responsible for calling `render_score()` to restore the HUD before resuming the game loop.

### Static elements drawn in `__init__`

The finish line is drawn once using a dedicated `Turtle` object in `__init__`. It persists for the lifetime of the window and is never cleared, because it is drawn by its own turtle — not by `_writer`. This means `_writer.clear()` (called by every overlay) cannot accidentally erase it.

---

## 11.1 Known Limitations

### Pause overlay z-ordering

The pause overlay text ("PAUSED" + options) can be obscured by cars when there are many on screen. The root cause is a turtle/tkinter constraint: `screen.update()` internally calls `canvas.tag_raise()` on every turtle's shape item on each call, which re-promotes all car polygons to the top of the canvas stack regardless of what was drawn on top of them. Standard fixes (raising the overlay rect and text via the canvas API after each update, lowering all polygon items before raising the overlay) were attempted but did not reliably hold between update cycles. A working solution would require either rendering the overlay in a separate tkinter widget or freezing the screen entirely (hiding all car turtles) during the overlay, both of which change the visual behaviour. Left as-is for now.

---

## 12. Course Context

**Course:** 100 Days of Code: The Complete Python Pro Bootcamp (Udemy — Dr. Angela Yu)
**Day:** 23
**Topic:** Turtle Crossing capstone — final project for the OOP section

The exercise introduced:
- Designing a multi-class system from scratch
- Separating game state across Player, CarManager, and Scoreboard
- Event-driven input with `onkey`
- Manual screen refresh with `tracer(0)` + `screen.update()`
- Using `time.sleep()` to control frame rate

The `original/` folder is the direct course output. The `advanced/` folder rebuilds it with a clean separation between logic and rendering, adds persistence, pause/overlay navigation, and the full title → game → title loop.

---

## 13. Dependencies

| Module | Used for |
|---|---|
| `turtle` | Screen, Turtle objects, rendering, event bindings |
| `tkinter` | Underlying GUI (used indirectly via turtle) |
| `time` | `time.sleep()` for tick rate and overlay delays |
| `random` | Car spawn chance and y-position selection |
| `sys` | `sys.exit(0)` for clean shutdown |
| `os` | `os.system()` for console clear in `menu.py` |
| `subprocess` | `subprocess.run()` to launch game builds from `menu.py` |
| `pathlib` | `Path(__file__).parent` for portable file paths |
