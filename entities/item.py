# entities/item.py

class Item:
    def __init__(self, name, image, position):
        self.name = name
        self.image = image
        self.position = position
        self.picked_up = False

    def draw(self, screen, camera):
        if not self.picked_up:
            screen.blit(
                self.image,
                (self.position[0] - camera.offset_x, self.position[1] - camera.offset_y)
            )
