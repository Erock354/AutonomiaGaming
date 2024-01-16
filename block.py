from object import *


# Defining Block class which inherits from the Object class
class Block(Object):

    # Initialize a Block object using specified x, y coordinates and size (both width and height are equal to size)
    def __init__(self, x, y, size):
        # 'super' keyword here makes sure the parent class (Object in this case) also gets initialized.
        super().__init__(x, y, size, size)
        self.rect = pygame.Rect(x, y, size, size)
