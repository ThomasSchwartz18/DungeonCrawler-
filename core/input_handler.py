# core/input_handler.py

from settings import TILE_SIZE
import pygame

def handle_input(scene):
    keys = pygame.key.get_pressed()
    dx, dy = 0, 0

    # Toggle inventory with Q key (only toggle if Q was previously released)
    if keys[pygame.K_q]:
        if not scene.q_pressed:  # Prevents toggling multiple times while Q is held down
            scene.inventory_open = not scene.inventory_open
            scene.q_pressed = True
    else:
        scene.q_pressed = False  # Reset when Q is released

    # Check for interaction with E key
    if keys[pygame.K_e] and not scene.inventory_open:
        if not scene.dagger_picked_up and player_near_dagger(scene):
            if scene.inventory.add_item("dagger", scene.dagger_image, to_hotbar=True):
                scene.dagger_picked_up = True

    # Check for punch with spacebar (if player has no weapon)
    if keys[pygame.K_SPACE] and not scene.inventory_open:
        if not scene.player.is_punching:
            scene.player.start_punch()
            
    # Take damage with H key (for testing)
    if keys[pygame.K_h]:  
        scene.player.take_damage(5)  # Decrease health by 5 each press
        
    # Hotbar selection (1-0 keys)
    for i, key in enumerate([pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5,
                             pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9, pygame.K_0]):
        if keys[key]:
            scene.inventory.select_hotbar_slot(i)
            selected_item = scene.inventory.get_selected_item()

            # Update the player's selected item
            if selected_item == "dagger":
                scene.player.set_selected_item("dagger")
            else:
                scene.player.set_selected_item(None)


    # Player movement
    if not scene.inventory_open:
        if keys[pygame.K_w]:
            dy = -1
        if keys[pygame.K_s]:
            dy = 1
        if keys[pygame.K_a]:
            dx = -1
        if keys[pygame.K_d]:
            dx = 1
        scene.player.set_movement(dx, dy)

def player_near_dagger(scene):
    player_rect = pygame.Rect(scene.player.x, scene.player.y, TILE_SIZE, TILE_SIZE)
    dagger_rect = pygame.Rect(scene.dagger_position[0], scene.dagger_position[1], TILE_SIZE, TILE_SIZE)
    return player_rect.colliderect(dagger_rect.inflate(30, 30))
