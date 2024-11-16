# utils.py

import pygame

def load_image(path, scale=(40, 40)):
    """Load an image from the specified path and scale it to the given size."""
    image = pygame.image.load(path).convert_alpha()
    return pygame.transform.scale(image, scale)
