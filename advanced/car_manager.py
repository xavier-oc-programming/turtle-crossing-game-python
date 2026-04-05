import random
from config import (
    CAR_COLORS,
    CAR_SPAWN_X,
    CAR_DESPAWN_X,
    CAR_Y_MIN,
    CAR_Y_MAX,
    CAR_SPAWN_CHANCE,
    STARTING_CAR_SPEED,
    SPEED_INCREMENT,
    COLLISION_WIDTH_MARGIN,
    COLLISION_HEIGHT_MARGIN,
)


class CarManager:
    """Pure logic: manages car positions and speeds.  No turtle, no UI."""

    def __init__(self) -> None:
        # Each car is a dict: {"x": float, "y": float, "color": str}
        self.cars: list[dict[str, float | str]] = []
        self.car_speed: float = STARTING_CAR_SPEED

    def create_car(self) -> None:
        if random.randint(1, CAR_SPAWN_CHANCE) == 1:
            self.cars.append({
                "x": float(CAR_SPAWN_X),
                "y": float(random.randint(CAR_Y_MIN, CAR_Y_MAX)),
                "color": random.choice(CAR_COLORS),
            })

    def move_cars(self) -> None:
        surviving: list[dict[str, float | str]] = []
        for car in self.cars:
            car["x"] = float(car["x"]) - self.car_speed
            if float(car["x"]) > CAR_DESPAWN_X:
                surviving.append(car)
        self.cars = surviving

    def increase_speed(self) -> None:
        self.car_speed += SPEED_INCREMENT

    def detect_collision(self, player_x: float, player_y: float) -> bool:
        for car in self.cars:
            cx = float(car["x"])
            cy = float(car["y"])
            if (
                player_x - COLLISION_WIDTH_MARGIN < cx < player_x + COLLISION_WIDTH_MARGIN
                and player_y - COLLISION_HEIGHT_MARGIN < cy < player_y + COLLISION_HEIGHT_MARGIN
            ):
                return True
        return False

    def reset(self) -> None:
        self.cars = []
        self.car_speed = STARTING_CAR_SPEED
