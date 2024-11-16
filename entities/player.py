import pygame
from settings import TILE_SIZE, HALF_TILE_SIZE, PLAYER_COLOR, DUNGEON_MAP, OFFSET_X, OFFSET_Y
from entities.spritesheet import SpriteStripAnim  # Import the SpriteStripAnim class

class Player:
    def __init__(self, x, y, speed=2, max_health=100):
        # Position and speed
        self.x = x * TILE_SIZE + (TILE_SIZE - HALF_TILE_SIZE) // 2
        self.y = y * TILE_SIZE + (TILE_SIZE - HALF_TILE_SIZE) // 2
        self.speed = speed

        # Health
        self.max_health = max_health
        self.current_health = max_health  # Start with full health
        self.is_dead = False  # Track whether the player is dead

        # Load animations
        self.idle_animation = SpriteStripAnim(
            "assets/character/idle/idle.png", 
            (0, 0, 25, 25), 
            4,  
            colorkey=None, 
            loop=True, 
            frames=10  
        )

        self.walk_animation = SpriteStripAnim(
            "assets/character/idle/walking.png", 
            (0, 0, 25, 25), 
            5,  
            colorkey=None, 
            loop=True, 
            frames=6  
        )

        self.punch_animation = SpriteStripAnim(
            "assets/character/punch.png", 
            (0, 0, 25, 25), 
            4,  
            colorkey=None, 
            loop=False, 
            frames=5  
        )

        self.death_animation = SpriteStripAnim(
            "assets/character/death.png", 
            (0, 0, 25, 25), 
            6,  # Number of frames in the death strip
            colorkey=None, 
            loop=False,  # Death animation does not loop
            frames=8  # Slightly slower animation
        )

        self.dagger_idle_animation = SpriteStripAnim(
            "assets/character/idle-dagger.png", 
            (0, 0, 25, 25), 
            5,  
            colorkey=None, 
            loop=True, 
            frames=10  
        )

        # Placeholder for current animation frame to draw
        self.current_frame = None  
        self.is_moving = False
        self.is_punching = False
        self.last_direction = 'right'  # Track the last horizontal direction ('left' or 'right')

        # Hotbar-related
        self.selected_item = None  # Track the currently selected item from the hotbar

    def can_move_to(self, new_x, new_y):
        """Check if the player can move to the specified pixel coordinates."""
        left_tile = int(new_x / TILE_SIZE)
        right_tile = int((new_x + HALF_TILE_SIZE - 1) / TILE_SIZE)
        top_tile = int(new_y / TILE_SIZE)
        bottom_tile = int((new_y + HALF_TILE_SIZE - 1) / TILE_SIZE)

        return (DUNGEON_MAP[top_tile][left_tile] == 0 and
                DUNGEON_MAP[top_tile][right_tile] == 0 and
                DUNGEON_MAP[bottom_tile][left_tile] == 0 and
                DUNGEON_MAP[bottom_tile][right_tile] == 0)

    def take_damage(self, amount):
        """Reduce the player's health by the specified amount."""
        if self.is_dead:
            return  # No damage if the player is already dead

        self.current_health = max(0, self.current_health - amount)

        # Check if the player has died
        if self.current_health == 0:
            self.is_dead = True
            self.death_animation.__iter__()  # Reset the death animation to the first frame

    def draw_health_bar(self, surface):
        """Draw the health bar at the bottom right of the screen."""
        if self.is_dead:
            return  # Do not draw health bar if the player is dead

        bar_width = 100  # Width of the health bar
        bar_height = 20  # Height of the health bar
        padding = 10     # Padding from the screen edge

        # Calculate the filled portion of the bar
        fill_ratio = self.current_health / self.max_health
        filled_bar_width = int(bar_width * fill_ratio)

        # Draw background bar (gray) and filled portion (green)
        bar_x = surface.get_width() - bar_width - padding
        bar_y = surface.get_height() - bar_height - padding
        pygame.draw.rect(surface, (100, 100, 100), (bar_x, bar_y, bar_width, bar_height))  # Background
        pygame.draw.rect(surface, (0, 255, 0), (bar_x, bar_y, filled_bar_width, bar_height))  # Filled portion

    def start_punch(self):
        """Start the punch animation."""
        if not self.is_punching and not self.is_dead:  # Prevent punching if dead
            self.is_punching = True
            self.punch_animation.__iter__()  # Reset the punch animation to the first frame

    def set_selected_item(self, item):
        """Set the currently selected item from the hotbar."""
        self.selected_item = item

    def update_animation(self):
        """Update the frame of the current animation based on movement, punch state, and selected item."""
        if self.is_dead:
            # Play death animation
            try:
                self.current_frame = next(self.death_animation)
            except StopIteration:
                pass  # Once the death animation finishes, it stays on the last frame
        elif self.is_punching:
            try:
                self.current_frame = next(self.punch_animation)
            except StopIteration:
                self.is_punching = False  # Stop punching once the animation finishes
        elif self.selected_item == "dagger" and not self.is_moving:
            # Use the dagger idle animation if dagger is selected and the player is idle
            try:
                self.current_frame = next(self.dagger_idle_animation)
            except StopIteration:
                self.dagger_idle_animation.__iter__()
                self.current_frame = next(self.dagger_idle_animation)
        elif self.is_moving:
            try:
                self.current_frame = next(self.walk_animation)
            except StopIteration:
                self.walk_animation.__iter__()
                self.current_frame = next(self.walk_animation)
        else:
            try:
                self.current_frame = next(self.idle_animation)
            except StopIteration:
                self.idle_animation.__iter__()
                self.current_frame = next(self.idle_animation)

    def update(self):
        """Update player state, including animations."""
        self.update_animation()

    def set_movement(self, dx, dy):
        """Set the movement direction and update position."""
        if self.is_dead:
            return  # Prevent movement if the player is dead

        self.is_moving = dx != 0 or dy != 0
        if dx > 0:
            self.last_direction = 'right'
        elif dx < 0:
            self.last_direction = 'left'

        # Horizontal movement
        if dx != 0:
            new_x = self.x + dx * self.speed
            if self.can_move_to(new_x, self.y):
                self.x = new_x

        # Vertical movement
        if dy != 0:
            new_y = self.y + dy * self.speed
            if self.can_move_to(self.x, new_y):
                self.y = new_y

    def draw(self, surface, camera):
        """Draw the player and health bar on the screen."""
        # Update animation frame
        self.update_animation()

        # Draw the current frame (idle, idle-dagger, walking, or punching)
        if self.current_frame is not None:
            frame_to_draw = pygame.transform.flip(self.current_frame, True, False) if self.last_direction == 'left' else self.current_frame
            frame_rect = frame_to_draw.get_rect(center=(self.x + HALF_TILE_SIZE // 2, self.y + HALF_TILE_SIZE // 2))
            frame_rect = camera.apply_to_rect(frame_rect)
            surface.blit(frame_to_draw, frame_rect)

        # Draw the health bar on the screen (if not dead)
        self.draw_health_bar(surface)
