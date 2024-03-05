import math

import pygame

from bullet import Bullet

from client import *


# Define a Player class that inherits pygame's Sprite class
class Player(pygame.sprite.Sprite):
    # STATIC GAME VARIABLE
    GRAVITY = 2
    SHOOTING_CD = 20
    HP = 100

    # Initialize a Player object with specified x, y coordinates and height and width of the player. Sets velocity
    # attributes on x and y coordinates to 0
    def __init__(self, x, y, height, width, color):
        super().__init__()
        self.color = color
        self.rect = pygame.Rect(x, y, height, width)
        self.x_vel = 0
        self.y_vel = 0
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.mask = pygame.mask.from_surface(self.image)
        self.direction = "left"
        self.fall_count = 0
        self.addr = None
        self.shoot_cd = 0  # Shooting cooldown

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
        self.shoot_cd -= 1  # Reloading

        # Draw Player on the game screen
    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)

    # Function to update Player state when they land from a jump
    def landed(self):
        self.fall_count = 0
        self.y_vel = 0

    # Function to update Player state when their head hits an obstacle while jumping
    def hit_head(self):
        self.fall_count = 0
        self.y_vel *= -1

    def shoot(self, client):

        mouse_cords = pygame.mouse.get_pos()
        x_change_mouse_player = (mouse_cords[0] - self.rect.centerx)
        y_change_mouse_player = (mouse_cords[1] - self.rect.centery)
        angle = math.degrees(math.atan2(y_change_mouse_player, x_change_mouse_player))

        if self.shoot_cd <= 0:                  # If cd is 0 player can shoot
            self.shoot_cd = self.SHOOTING_CD    # Shooting reset otherwise u can spam shooting

            bullet = Bullet(self.rect.centerx - 16, self.rect.centery - 16, angle, 25)
            # -16 on the X and the Y coordinates are used to fix the bullet spawning point (the bullet start point
            # will be the center of the player)
            client.send_bullet(bullet)

