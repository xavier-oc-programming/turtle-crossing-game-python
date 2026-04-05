import time
from turtle import Screen
from player import Player
from car_manager import CarManager
from scoreboard import Scoreboard

# Constants for collision detection
COLLISION_WIDTH_MARGIN = 25  # Covers the width (including edges)
COLLISION_HEIGHT_MARGIN = 30  # Covers the height (including the head)

# Set up the screen
screen = Screen()
screen.setup(width=600, height=600)
screen.tracer(0)

# Create game objects
player = Player()
car_manager = CarManager()
scoreboard = Scoreboard()

# Bind player movement to the "Up" arrow key
screen.listen()
screen.onkey(player.move_up, "Up")

# Main game loop
game_is_on = True
while game_is_on:
    time.sleep(0.032)  # 60 FPS refresh rate
    screen.update()

    # Generate and move cars
    car_manager.create_car()
    car_manager.move_cars()

    # Detect collision with cars
    for car in car_manager.all_cars:
        if (
            player.xcor() - COLLISION_WIDTH_MARGIN < car.xcor() < player.xcor() + COLLISION_WIDTH_MARGIN
            and player.ycor() - COLLISION_HEIGHT_MARGIN < car.ycor() < player.ycor() + COLLISION_HEIGHT_MARGIN
        ):
            scoreboard.game_over()  # Display "GAME OVER"
            game_is_on = False      # Stop the game loop

    # Detect if the player successfully crosses to the finish line
    if player.ycor() > 280:
        player.reset_position()
        car_manager.level_up()
        scoreboard.increase_level()

# Keep the screen open and wait for user click to exit
screen.exitonclick()
