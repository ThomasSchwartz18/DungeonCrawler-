# scenes/main_scene.py

import pygame
import sys
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, BG_COLOR, FPS, TILE_SIZE, WALL_IMAGE_1, WALL_IMAGE_2, TILE_IMAGE_1
from entities.player import Player
from core.camera import Camera
from core.dungeon import render_static_dungeon
from core.inventory import Inventory
from core.utils import load_image
from core.input_handler import handle_input

class MainScene:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Simple Dungeon Crawler")
        self.clock = pygame.time.Clock()
        
        # Load assets
        wall_image_1 = load_image(WALL_IMAGE_1, (TILE_SIZE, TILE_SIZE))
        wall_image_2 = load_image(WALL_IMAGE_2, (TILE_SIZE, TILE_SIZE))
        ground_image = load_image(TILE_IMAGE_1, (TILE_SIZE, TILE_SIZE))
        wall_image_1.set_colorkey((0, 0, 0))
        wall_image_2.set_colorkey((0, 0, 0))
        ground_image.set_colorkey((0, 0, 0))  # Set black as transparent

        # Load the dagger image and store it in self.dagger_image
        self.dagger_image = load_image("assets/weapons/dagger.png", (TILE_SIZE, TILE_SIZE)).convert_alpha()

        # Initialize game components
        self.dungeon_surface = render_static_dungeon(wall_image_1, wall_image_2, ground_image)
        self.player = Player(x=1, y=1, speed=1.5)
        self.camera = Camera()
        self.inventory = Inventory()  # Inventory handles both the hotbar and grid
        self.dagger_position = (5 * TILE_SIZE, 5 * TILE_SIZE)
        self.dagger_picked_up = False
        self.inventory_open = False  # State of the inventory
        self.q_pressed = False  # To track if Q is being held down

    def run(self):
        """Main game loop."""
        running = True
        while running:
            self.screen.fill(BG_COLOR)

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Handle input
            handle_input(self)

            # Update game state
            self.update()

            # Render the game
            self.render()

            # Update the display
            pygame.display.flip()
            self.clock.tick(FPS)

    def update(self):
        """Update game state and check interactions."""
        mouse_pos = pygame.mouse.get_pos()

        # Update inventory (hotbar is always updated)
        self.inventory.update(mouse_pos, self.inventory_open)

        if not self.inventory_open:
            self.camera.update(self.player)
        self.player.update()  # Update player animation and state

    def render(self):
        """Render the game scene."""
        # Draw the dungeon and the player
        self.draw_dungeon()
        
        # Draw the player (including the health bar)
        self.player.draw(self.screen, self.camera)

        # Draw the dagger if it hasn't been picked up
        if not self.dagger_picked_up:
            dagger_screen_x = self.dagger_position[0] - self.camera.offset_x
            dagger_screen_y = self.dagger_position[1] - self.camera.offset_y
            self.screen.blit(self.dagger_image, (dagger_screen_x, dagger_screen_y))

        # Always draw the hotbar
        self.inventory.draw_hotbar(self.screen)

        # Draw the inventory if it's open
        if self.inventory_open:
            self.inventory.draw(self.screen, inventory_open=True)

    def draw_dungeon(self):
        """Draw the dungeon surface with camera offset."""
        scaled_dungeon = pygame.transform.scale(
            self.dungeon_surface,
            (int(self.dungeon_surface.get_width() * self.camera.zoom),
             int(self.dungeon_surface.get_height() * self.camera.zoom))
        )
        dungeon_rect = scaled_dungeon.get_rect()
        dungeon_rect.topleft = (-self.camera.offset_x, -self.camera.offset_y)
        self.screen.blit(scaled_dungeon, dungeon_rect)
