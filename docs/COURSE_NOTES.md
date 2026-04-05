# Course Notes — Day 23: Turtle Crossing

## Exercise description

**Course:** 100 Days of Code: The Complete Python Pro Bootcamp (Udemy — Dr. Angela Yu)
**Day:** 23
**Topic:** Building a Turtle Crossing (Frogger-style) game — capstone project for the OOP section

---

## Brief

Build a Frogger-style crossing game using Python's `turtle` module.
The player controls a turtle that must cross a road full of moving cars.
Each successful crossing increases the level and car speed.

### Requirements set by the course

1. **Screen setup** — 600 × 600 window, tracer off for manual refresh control.
2. **Player** — turtle shape starting at the bottom centre; moves upward with the Up arrow key.
3. **Cars** — random colours, spawning from the right side at random y-positions; 1-in-6 chance per frame.
4. **Collision detection** — game ends when the player turtle overlaps a car.
5. **Level up** — when the player reaches the top (y > 280), they reset to the bottom and level increments.
6. **Speed increase** — car speed increases by a fixed amount on each level up.
7. **Scoreboard** — displays current level in the top-left corner; shows "GAME OVER" on collision.

### Key OOP concepts practised

- Class inheritance (`Player`, `Scoreboard` extend `Turtle`)
- Composition (`CarManager` owns a list of Turtle objects)
- Encapsulation — each class manages its own state and behaviour
- Separation of concerns across multiple files
- Event-driven input with `onkey`

---

## Original file layout (course state)

```
main.py        — screen setup, game loop, collision logic
player.py      — Player class (movement, reset)
car_manager.py — CarManager class (spawn, move, level up)
scoreboard.py  — Scoreboard class (display, level, game over)
```

---

## Notes on deviations from the course

The files in `original/` are kept as close as possible to the course state.
The only permitted change was fixing any hard-coded file paths to use
`Path(__file__).parent` so the game can be launched from the root `menu.py`
without breaking relative imports or data reads.
In practice the original has no file I/O, so **no changes were needed**.
