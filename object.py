import pygame.sprite


class Object(pygame.sprite.Sprite):
    COLOR = (0, 0, 0)

    def __init__(self, x, y, width, height, name=None):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.width = width
        self.height = height
        self.name = name

    def draw(self, win):
        pygame.draw.rect(win, self.COLOR, self.rect)

