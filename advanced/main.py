import time

from player import Player
from car_manager import CarManager
from scoreboard import Scoreboard
from display import Display
from config import GAME_TICK


class GameState:
    """Wraps all logic objects.  reset() returns everything to starting state."""

    def __init__(self) -> None:
        self.player: Player = Player()
        self.car_manager: CarManager = CarManager()

    def reset(self) -> None:
        self.player.reset_to_start()
        self.car_manager.reset()


def main() -> None:
    state = GameState()
    tracker = Scoreboard()
    display = Display()

    # ------------------------------------------------------------------
    # Outer loop — returns here (same window) whenever R is pressed
    # ------------------------------------------------------------------
    while True:
        state.reset()
        tracker.reset()

        # Render starting positions BEFORE show_welcome so objects appear
        # at the right place when revealed after the title screen
        display.render_player(state.player.x, state.player.y)
        display.render_cars(state.car_manager.cars)
        display.render_score(tracker.level, tracker.high_score)
        display.screen.update()

        mode = display.show_welcome()   # "start" | None (Q = quit)
        if mode is None:
            display.close()             # sys.exit(0) — only true quit path

        # show_welcome() calls _writer.clear() at the end, wiping the HUD.
        # Redraw it immediately so the score is visible before the first tick.
        display.render_score(tracker.level, tracker.high_score)
        display.screen.update()

        # --------------------------------------------------------------
        # Key state
        # --------------------------------------------------------------
        keys: dict[str, bool] = {"up": False, "pause": False}

        def press_up() -> None:         keys["up"] = True
        def release_up() -> None:       keys["up"] = False
        def trigger_pause() -> None:    keys["pause"] = True

        display.screen.onkeypress(press_up,       "Up")
        display.screen.onkeyrelease(release_up,   "Up")
        display.screen.onkeypress(trigger_pause,  "space")
        display.screen.listen()

        # --------------------------------------------------------------
        # Inner loop — break → outer loop → title screen
        # --------------------------------------------------------------
        while True:
            time.sleep(GAME_TICK)
            display.screen.update()

            # --- Pause check (BEFORE moving anything) -----------------
            if keys["pause"]:
                keys["pause"] = False
                # Unregister Space BEFORE entering overlay so it cannot
                # fire the pause handler while we are inside show_pause()
                display.screen.onkeypress(None, "space")
                if not display.show_pause():
                    break               # R → title screen
                # Re-register Space for pause and re-call listen()
                display.screen.onkeypress(trigger_pause, "space")
                display.screen.listen()
                # Restore HUD that show_pause()._writer.clear() wiped
                display.render_score(tracker.level, tracker.high_score)
                display.screen.update()

            # --- Logic ------------------------------------------------
            if keys["up"]:
                state.player.move_up()

            state.car_manager.create_car()
            state.car_manager.move_cars()

            # --- Render -----------------------------------------------
            display.render_player(state.player.x, state.player.y)
            display.render_cars(state.car_manager.cars)

            # --- Collision check --------------------------------------
            if state.car_manager.detect_collision(state.player.x, state.player.y):
                new_high = tracker.is_new_high_score()   # check BEFORE saving
                tracker.save_high_score()

                display.render_score(tracker.level, tracker.high_score)  # update BEFORE overlay
                display.screen.onkeypress(None, "space")

                if not display.show_game_over(tracker.level, tracker.high_score, new_high):
                    break               # R → title screen

                # Play again — reset state and restart inner loop
                state.reset()
                tracker.reset()
                display.render_player(state.player.x, state.player.y)
                display.render_cars(state.car_manager.cars)
                display.render_score(tracker.level, tracker.high_score)
                display.screen.update()
                display.screen.onkeypress(trigger_pause, "space")
                display.screen.listen()
                continue

            # --- Crossing check ---------------------------------------
            if state.player.has_crossed():
                tracker.increment_level()
                state.car_manager.increase_speed()
                state.player.reset_to_start()

                # Flash level-up message (wipes _writer, so redraw HUD after)
                display.show_level_up(tracker.level)
                display.render_score(tracker.level, tracker.high_score)
                display.render_player(state.player.x, state.player.y)
                display.screen.update()

        # Inner loop broke → outer loop continues → title screen


if __name__ == "__main__":
    main()
