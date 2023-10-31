import pygame


class Player(pygame.sprite.Sprite):
    COLOR = (255, 0, 0)
    GRAVITY = 1

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

    def jump(self, objects):
        for obj in objects:
            if self.rect.bottom == obj.rect.top:
                self.y_vel = -self.GRAVITY * 8

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def move_left(self, vel):
        self.x_vel = -vel
        if self.direction != "left":
            self.direction = "left"

    def move_right(self, vel):
        self.x_vel = vel
        if self.direction != "right":
            self.direction = "right"

    def loop(self, fps):
        self.y_vel += min(1, (self.fall_count / fps) * self.GRAVITY)
        self.move(self.x_vel, self.y_vel)
        self.fall_count += 1

    def draw(self, win):
        pygame.draw.rect(win, self.COLOR, self.rect)

    def landed(self):
        self.fall_count = 0
        self.y_vel = 0

    def hit_head(self):
        self.fall_count = 0
        self.y_vel *= -1

