# main.py

import pygame
from scenes.main_scene import MainScene

def main():
    # Initialize pygame
    pygame.init()

    # Run the main scene (game loop)
    main_scene = MainScene()
    main_scene.run()

if __name__ == "__main__":
    main()
