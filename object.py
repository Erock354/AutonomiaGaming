import pygame.sprite


# Define an Object class that inherits from pygame's Sprite class
class Object(pygame.sprite.Sprite):
    # Setting a default color for the object
    COLOR = (0, 0, 0)

    # Initialize an Object with specified x, y coordinates and height, with and optional name. The color of the
    # object is defined by the COLOR attribute.
    def __init__(self, x, y, width, height, name=None):
        super().__init__()  # Call to the base class's constructor
        self.rect = pygame.Rect(x, y, width, height)
        # Create an image object using pygame’s Surface method
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.width = width
        self.height = height
        # Name of the object (optional)
        self.name = name

    # Method to draw the Object on the game screen
    def draw(self, win):
        pygame.draw.rect(win, self.COLOR, self.rect)
