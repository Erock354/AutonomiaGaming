from object import *


class Block(Object):

    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        self.mask = pygame.mask.from_surface(self.image)
