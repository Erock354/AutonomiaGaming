import pygame


# Define a Player class that inherits pygame's Sprite class
class Player(pygame.sprite.Sprite):
    # Set a color and gravity constant for Player
    COLOR = (255, 0, 0)
    GRAVITY = 1

    # Initialize a Player object with specified x, y coordinates and height and width of the player. Sets velocity
    # attributes on x and y coordinates to 0
    def __init__(self, x, y, height, width):
        super().__init__()
        self.rect = pygame.Rect(x, y, height, width)
        self.x_vel = 0
        self.y_vel = 0
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.mask = pygame.mask.from_surface(self.image)
        self.direction = "left"
        self.fall_count = 0
        self.addr = None

    # Function to make the player jump, increases y_velocity depending on the gravity
    def jump(self, objects):
        for obj in objects:
            if self.rect.bottom == obj.rect.top:
                self.y_vel = -self.GRAVITY * 8

    # Move function updates x, y coordinates of Player
    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    # Function to allow the player to move left, takes velocity as argument
    def move_left(self, vel):
        self.x_vel = -vel
        if self.direction != "left":
            self.direction = "left"

    # Function to allow the player to move right, takes velocity as argument
    def move_right(self, vel):
        self.x_vel = vel
        if self.direction != "right":
            self.direction = "right"

    # Loop function to deal with changing game physics such as player falling
    def loop(self, fps):
        self.y_vel += min(1, (self.fall_count / fps) * self.GRAVITY)
        self.move(self.x_vel, self.y_vel)
        self.fall_count += 1

    # Draw Player on the game screen
    def draw(self, win):
        pygame.draw.rect(win, self.COLOR, self.rect)

    # Function to update Player state when they land from a jump
    def landed(self):
        self.fall_count = 0
        self.y_vel = 0

    # Function to update Player state when their head hits an obstacle while jumping
    def hit_head(self):
        self.fall_count = 0
        self.y_vel *= -1
