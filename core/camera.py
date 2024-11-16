# camera.py

import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, ZOOM

class Camera:
    def __init__(self):
        self.zoom = ZOOM
        self.offset_x = 0
        self.offset_y = 0
        self.smooth_factor = 0.1  # Smooth movement factor

    def update(self, player):
        """Update the camera's position smoothly to keep the player centered."""
        target_x = player.x * self.zoom - SCREEN_WIDTH // 2
        target_y = player.y * self.zoom - SCREEN_HEIGHT // 2

        # Lerp towards the target position for smooth movement
        self.offset_x += (target_x - self.offset_x) * self.smooth_factor
        self.offset_y += (target_y - self.offset_y) * self.smooth_factor

        # Round the offset to the nearest integer to avoid fractional pixels
        self.offset_x = round(self.offset_x)
        self.offset_y = round(self.offset_y)

    def apply(self, position):
        """Apply camera offset and zoom to a given position."""
        x, y = position
        return ((x * self.zoom) - self.offset_x, (y * self.zoom) - self.offset_y)

    def apply_to_rect(self, rect):
        """Apply camera offset and zoom to a given rectangle."""
        rect.x = rect.x * self.zoom - self.offset_x
        rect.y = rect.y * self.zoom - self.offset_y
        rect.width *= self.zoom
        rect.height *= self.zoom
        return rect
