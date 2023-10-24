import pygame

from block import Block
from player import *

from client import *

pygame.init()
pygame.display.set_caption("IDK MAN")

HEIGHT = 500
WIDTH = 500
PLAYER_VEL = 5
FPS = 180
clock = pygame.time.Clock()

screen = pygame.display.set_mode([HEIGHT, WIDTH])


def draw(win, player, objects):
    screen.fill("white")

    for obj in objects:
        obj.draw(win)

    player.draw(win)
    pygame.display.update()


def handle_vertical_collision(player, objects, dy):
    collided_objects = []
    for obj in objects:
        if pygame.sprite.collide_rect(player, obj):
            if dy > 0:
                player.rect.bottom = obj.rect.top
                player.landed()
            elif dy < 0:
                player.rect.top = obj.rect.bottom
                player.hit_head()
        collided_objects.append(obj)

    return collided_objects


def handle_movement(player, objects):
    player.x_vel = 0

    keys = pygame.key.get_pressed()

    if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and not player.rect.left <= 0:
        player.move_left(PLAYER_VEL)
    if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and not player.rect.right >= WIDTH:
        player.move_right(PLAYER_VEL)

    handle_horizontal_collision(player, objects)
    handle_vertical_collision(player, objects, player.y_vel)


def handle_horizontal_collision(player, objects):
    pass


def main():
    running = True
    block_size = 64
    player = Player(100, 64, block_size, block_size)

    threads = connect(player)

    floor = [Block(i * block_size, HEIGHT - block_size, block_size) for i in
             range(-WIDTH // block_size, WIDTH * 2 // block_size)]

    objects = [*floor, Block(0, HEIGHT - block_size * 2, block_size)]

    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.jump(objects=objects)

        player.loop(FPS)
        handle_movement(player, objects)
        draw(win=screen, player=player, objects=objects)
        
    pygame.quit()


if __name__ == "__main__":
    main()
