import pygame

class spritesheet:
    def __init__(self, filename):
        try:
            self.sheet = pygame.image.load(filename).convert_alpha()
        except pygame.error as message:
            print('Unable to load spritesheet image:', filename)
            raise SystemExit(message)

    def image_at(self, rectangle, colorkey=None):
        """Loads image from x,y,x+offset,y+offset"""
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size, pygame.SRCALPHA).convert_alpha()
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image

    def images_at(self, rects, colorkey=None):
        """Loads multiple images, supply a list of coordinates"""
        return [self.image_at(rect, colorkey) for rect in rects]

    def load_strip(self, rect, image_count, colorkey=None):
        """Loads a strip of images and returns them as a list"""
        tups = [(rect[0] + rect[2] * x, rect[1], rect[2], rect[3]) for x in range(image_count)]
        return self.images_at(tups, colorkey)

class SpriteStripAnim:
    """Sprite strip animator with Python iterator protocol."""

    def __init__(self, filename, rect, count, colorkey=None, loop=False, frames=1, target_size=(35,35)):
        """
        filename: path to the spritesheet image
        rect: rectangle specifying the location and size of the first frame
        count: number of frames in the strip
        colorkey: color to treat as transparent
        loop: whether the animation should loop
        frames: number of ticks each frame should stay on screen
        target_size: (width, height) tuple for resizing each frame (optional)
        """
        self.filename = filename
        ss = spritesheet(filename)
        self.images = ss.load_strip(rect, count, colorkey)

        # Resize frames if target_size is specified
        if target_size is not None:
            self.images = [pygame.transform.scale(img, target_size) for img in self.images]

        self.i = 0
        self.loop = loop
        self.frames = frames
        self.f = frames

    def __iter__(self):
        """Return the iterator object itself."""
        self.i = 0
        self.f = self.frames
        return self

    def __next__(self):
        """Return the next frame in the animation."""
        if self.i >= len(self.images):
            if not self.loop:
                raise StopIteration
            else:
                self.i = 0
        image = self.images[self.i]
        self.f -= 1
        if self.f == 0:
            self.i += 1
            self.f = self.frames
        return image
