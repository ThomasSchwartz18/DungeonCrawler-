# settings.py

import os

# Screen settings
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700
TILE_SIZE = 40
HALF_TILE_SIZE = TILE_SIZE // 2  # Half size for player
QUART_TILE_SIZE = TILE_SIZE // 3
TENTH_TILE_SIZE = TILE_SIZE // 10

# Colors
PLAYER_COLOR = (0, 255, 0)
BG_COLOR = (0, 0, 0)

# Frame rate
FPS = 60

# Camera settings
ZOOM = 1.5  # Zoom factor; 2 means 2x zoom
CAMERA_CENTER_X = SCREEN_WIDTH // 2
CAMERA_CENTER_Y = SCREEN_HEIGHT // 2

# Key mappings for movement
MOVE_KEYS = {
    'UP': (0, -1),
    'DOWN': (0, 1),
    'LEFT': (-1, 0),
    'RIGHT': (1, 0)
}

# Dungeon map layout (1 = wall, 0 = floor)
DUNGEON_MAP = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1],
    [1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]


# Calculate dungeon dimensions
DUNGEON_WIDTH = len(DUNGEON_MAP[0]) * TILE_SIZE
DUNGEON_HEIGHT = len(DUNGEON_MAP) * TILE_SIZE

# Calculate offsets to center the dungeon
OFFSET_X = (SCREEN_WIDTH - DUNGEON_WIDTH) // 2
OFFSET_Y = (SCREEN_HEIGHT - DUNGEON_HEIGHT) // 2

# Paths to assets
ASSET_PATH = os.path.join("assets")
WALL_IMAGE_1 = os.path.join(ASSET_PATH, "wall1.png")
WALL_IMAGE_2 = os.path.join(ASSET_PATH, "wall2.png")
TILE_IMAGE_1 = os.path.join(ASSET_PATH, "tile1.png")

# Flashlight effect settings
FLASHLIGHT_RADIUS = 150       # Radius of the flashlight beam in pixels
FLASHLIGHT_COLOR = (0, 0, 0, 180)  # Dark color with some transparency (RGBA)