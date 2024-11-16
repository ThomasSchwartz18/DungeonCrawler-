# core/dungeon.py

import pygame
from settings import TILE_SIZE, DUNGEON_MAP

def render_static_dungeon(wall_image_1, wall_image_2, ground_image):
    """Render the entire dungeon onto a single surface with walls and ground textures."""
    dungeon_width = len(DUNGEON_MAP[0]) * TILE_SIZE
    dungeon_height = len(DUNGEON_MAP) * TILE_SIZE
    dungeon_surface = pygame.Surface((dungeon_width, dungeon_height))

    # Draw each tile on the dungeon surface
    for y, row in enumerate(DUNGEON_MAP):
        for x, tile in enumerate(row):
            if tile == 1:  # Draw wall
                # Alternate between wall images based on the x, y position (checkerboard pattern)
                wall_image = wall_image_1 if (x + y) % 2 == 0 else wall_image_2
                dungeon_surface.blit(wall_image, (x * TILE_SIZE, y * TILE_SIZE))
            else:  # Draw ground
                dungeon_surface.blit(ground_image, (x * TILE_SIZE, y * TILE_SIZE))

    return dungeon_surface
