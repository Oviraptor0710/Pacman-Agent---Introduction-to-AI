ALGORITHM: str = "MINIMAX"

LEVEL_TO_ALGORITHM = {
    "LEVEL1": "BFS",
    "LEVEL2": "Local Search",
    "LEVEL3": "Minimax"
}

# DEFINE COLOR
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
PURPLE = (255, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
WALL_DEEP_BLUE = (25, 25, 166)
WALL_ELECTRIC_BLUE = (0, 153, 255)
WALL_PURPLE = (93, 63, 211)


FOOD_PINK = (224, 102, 255)        # Bright classic yellow
FOOD_WHITE = (255, 255, 255)       # Clean white dots
FOOD_ORANGE = (255, 192, 76)       #


# DEFINE MAP
SIZE_WALL: int = 40
DEFINE_WIDTH: int = 6
BLOCK_SIZE: int = SIZE_WALL // 2

# Entity
EMPTY = 0
WALL = 1
FOOD = 2
MONSTER = 3

# Setup screen
WIDTH: int = 1200
HEIGHT: int = 600
FPS: int = 300

MARGIN = {
    "TOP": 0,
    "LEFT": 0
}


import os

# Đường dẫn đến thư mục Source/Images
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMAGE_DIR = os.path.join(BASE_DIR, "Images")

# IMAGE
IMAGE_GHOST = [ 
    os.path.join(IMAGE_DIR, "Inky.png"),
    os.path.join(IMAGE_DIR, "Clyde.png"),
    os.path.join(IMAGE_DIR, "Blinky.png"), 
    os.path.join(IMAGE_DIR, "Pinky.png")
]
IMAGE_PACMAN = [
    os.path.join(IMAGE_DIR, "1.png"), 
    os.path.join(IMAGE_DIR, "2.png"), 
    os.path.join(IMAGE_DIR, "3.png"), 
    os.path.join(IMAGE_DIR, "4.png")
]