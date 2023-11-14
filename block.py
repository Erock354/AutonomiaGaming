from object import *


# Defining Block class which inherits from the Object class
class Block(Object):

    # Initialize a Block object using specified x, y coordinates and size (both width and height are equal to size)
    def __init__(self, x, y, size):
        # 'super' keyword here makes sure the parent class (Object in this case) also gets initialized.
        super().__init__(x, y, size, size)
        # Creating a mask for pixel-perfect collision detection. The mask is basically an image with a lot of
        # 'points'. It uses this image to precisely detect collisions rather than relying on the boundary of the
        # rectangular image.
        self.mask = pygame.mask.from_surface(self.image)
