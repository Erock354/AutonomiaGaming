import pygame
import math


class Bullet(pygame.sprite.Sprite):
    BULLET_SCALE = 32
    BULLET_SPEED = 16
    BULLET_LIFETIME = 720

    def __init__(self, x, y, angle, dmg):
        super().__init__()
        self.dmg = dmg
        self.rect = pygame.Rect(x, y, self.BULLET_SCALE, self.BULLET_SCALE)
        self.rect.center = (x, y)
        self.color = "black"
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = self.BULLET_SPEED
        self.x_vel = math.cos(self.angle * (2 * math.pi / 360)) * self.speed
        self.y_vel = math.sin(self.angle * (2 * math.pi / 360)) * self.speed
        self.bullet_lifetime = self.BULLET_LIFETIME
        self.spawn_time = pygame.time.get_ticks()  # gets the specific time that the bullet was created

    def bullet_movement(self):
        self.x += self.x_vel
        self.y += self.y_vel

        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

        if pygame.time.get_ticks() - self.spawn_time > self.bullet_lifetime:
            self.kill()

    def update(self, win):
        self.bullet_movement()

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)
