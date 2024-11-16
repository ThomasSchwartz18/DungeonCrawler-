import pygame

# Slot class to represent each slot in the inventory
class Slot:
    def __init__(self, x, y, size=50, border_image=None):
        self.x = x
        self.y = y
        self.size = size
        self.item = None  # Holds the item in the slot (could be an image or item ID)
        self.item_id = None  # Holds the identifier for the item (e.g., "dagger")
        self.border_image = border_image  # Optional border image (only used for hotbar slots)

    def draw(self, win, is_selected=False):
        # Draw the border image (if it exists)
        if self.border_image:
            # Scale the border image to match the slot size
            scaled_border = pygame.transform.scale(self.border_image, (self.size, self.size))
            win.blit(scaled_border, (self.x, self.y))

        # Highlight the slot if selected
        if is_selected:
            pygame.draw.rect(win, (255, 255, 0), (self.x, self.y, self.size, self.size), 3)  # Yellow border for selected

        # If there is an item in the slot, draw it
        if self.item:
            # Scale the item image to fit within the slot with padding
            scaled_item = pygame.transform.scale(self.item, (self.size - 10, self.size - 10))
            item_rect = scaled_item.get_rect(center=(self.x + self.size // 2, self.y + self.size // 2))
            win.blit(scaled_item, item_rect)
            
        # Draw slot rectangle (optional background color for empty slots)
        color = (255, 0, 0) if is_selected else (200, 200, 200)  # Red if selected, gray otherwise
        pygame.draw.rect(win, color, (self.x, self.y, self.size, self.size), 0)  # Filled rectangle

        # If there is an item in the slot, draw it
        if self.item:
            # Draw the item image slightly inset for padding
            item_rect = self.item.get_rect()
            item_rect.topleft = (self.x + 5, self.y + 5)  # Add padding
            win.blit(self.item, item_rect)


# Inventory class to manage the inventory system
class Inventory:
    def __init__(self, rows=5, cols=10, cell_size=50, padding=10, start_x=10, start_y=10):
        """
        Initializes the inventory system. Default positions are adjusted
        to move the hotbar and inventory closer to the top-left corner.

        :param rows: Number of rows in the inventory
        :param cols: Number of columns in the inventory
        :param cell_size: Size of each inventory slot
        :param padding: Padding between slots
        :param start_x: Starting X position for the inventory grid
        :param start_y: Starting Y position for the inventory grid
        """
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.padding = padding
        self.start_x = start_x  # X offset for the grid
        self.start_y = start_y  # Y offset for the grid
        self.slots = []  # All inventory slots (including hotbar row)
        self.selected_slot = None  # Selected slot based on mouse position
        self.selected_hotbar_slot = 0  # Hotbar slot selected by number keys (default: first slot)

        # Load the hotbar border image
        try:
            self.hotbar_border_image = pygame.image.load("assets/inventory/hotbar-box.png").convert_alpha()
            print("Hotbar border image loaded successfully")
        except pygame.error as e:
            print(f"Failed to load hotbar border image: {e}")
            self.hotbar_border_image = None  # Fallback in case of failure

        # Create slots based on the grid dimensions
        self.create_slots()

    def create_slots(self):
        """Populate the inventory with Slot objects."""
        for row in range(self.rows):
            for col in range(self.cols):
                x = self.start_x + col * (self.cell_size + self.padding)
                y = self.start_y + row * (self.cell_size + self.padding)

                # Apply the hotbar border image only to the first row (hotbar)
                if row == 0:  # Hotbar row
                    self.slots.append(Slot(x, y, self.cell_size, border_image=self.hotbar_border_image))
                else:  # Other inventory rows
                    self.slots.append(Slot(x, y, self.cell_size))

    def update(self, mouse_pos, inventory_open):
        """Update the selected slot based on the mouse position."""
        mx, my = mouse_pos
        self.selected_slot = None  # Reset selected slot at the start of each update

        # Check for selection only if inventory is open
        if inventory_open:
            for index, slot in enumerate(self.slots):
                if self.collision(slot.x, slot.y, mx, my, slot.size, slot.size):
                    self.selected_slot = index
                    return

    def draw(self, win, inventory_open):
        """Draw the inventory grid and hotbar on the screen."""
        # Always draw the hotbar (first row of slots)
        self.draw_hotbar(win)

        # Draw the rest of the inventory only if open
        if inventory_open:
            for index, slot in enumerate(self.slots[self.cols:]):  # Skip the first row (hotbar)
                is_selected = (index + self.cols == self.selected_slot)  # Adjust index for selection
                slot.draw(win, is_selected)

    def draw_hotbar(self, win):
        """Draw the hotbar, which mirrors the first row of the inventory."""
        for index in range(self.cols):  # Only draw the first row of slots
            slot = self.slots[index]
            is_selected = (index == self.selected_hotbar_slot)  # Highlight the selected hotbar slot
            slot.draw(win, is_selected=is_selected)

    def collision(self, x, y, mx, my, w, h):
        """Check if the mouse is over a slot."""
        return x < mx < x + w and y < my < y + h

    def select_hotbar_slot(self, slot_index):
        """Select a specific hotbar slot (0-9)."""
        if 0 <= slot_index < self.cols:
            self.selected_hotbar_slot = slot_index

    def get_selected_item(self):
        """Get the identifier of the item in the currently selected hotbar slot."""
        selected_slot = self.slots[self.selected_hotbar_slot]
        print(f"Selected hotbar item: {selected_slot.item_id if selected_slot else None}")  # Debugging
        return selected_slot.item_id if selected_slot else None

    def add_item(self, item_id, item_image, to_hotbar=False):
        """
        Add an item to the inventory.
        
        :param item_id: The identifier for the item (e.g., "dagger").
        :param item_image: The image associated with the item.
        :param to_hotbar: If True, prioritize placing the item in the hotbar row.
        :return: True if the item was successfully added, False if no space is available.
        """
        slots = self.slots[:self.cols] if to_hotbar else self.slots  # Prioritize hotbar if needed
        for slot in slots:
            if slot.item is None:  # Find the first empty slot
                slot.item = item_image  # Set the item's image
                slot.item_id = item_id  # Set the item's identifier
                return True
        return False  # Return False if no empty slot was found