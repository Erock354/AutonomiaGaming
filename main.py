import pygame

from block import Block
from client import *

# Initialize pygame and set a title for the window
pygame.init()
pygame.display.set_caption("IDK MAN")

# Define some global constants like HEIGHT, WIDTH, PLAYER_VEL (player_velocity), FPS (frames_per_second), clock (used
# for setting game clock), and screen (main game window)
HEIGHT = 500
WIDTH = 500
PLAYER_VEL = 5
FPS = 180
clock = pygame.time.Clock()
screen = pygame.display.set_mode([HEIGHT, WIDTH])


# Function to draw the game objects on the game window
def draw(win, other_players, objects):
    screen.fill("white")  # Fill the game screen with white color

    # Draw the static game objects 
    for obj in objects:
        obj.draw(win)

    # Draw the online players on the screen
    for player in other_players:
        player.draw(win)

    # Update the game display after drawing the objects
    pygame.display.update()


# Function to handle vertical collisions on the game objects
def handle_vertical_collision(player, objects, dy):
    collided_objects = []
    for obj in objects:
        if pygame.sprite.collide_rect(player, obj):
            if dy > 0:  # If the player is falling
                player.rect.bottom = obj.rect.top  # Set the player's bottom to the object's top
                player.landed()  # Set the player's fall count to 0
            elif dy < 0:  # If the player is jumping
                player.rect.top = obj.rect.bottom  # Set the player's top to the object's bottom
                player.hit_head()  # Set the player's fall count to 0 and reverse the player's y velocity
        collided_objects.append(obj)
    return collided_objects


# Function to handle player movements and player collision with game objects
def handle_movement(player, objects):
    player.x_vel = 0
    keys = pygame.key.get_pressed()  # Get the list of pressed keys


    collide_left = collide(player, objects, -PLAYER_VEL)
    collide_right = collide(player, objects, PLAYER_VEL)

    # Handle left and right player movements
    if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and not player.rect.left <= 0 and not collide_left:
        player.move_left(PLAYER_VEL)
    if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and not player.rect.right >= WIDTH and not collide_right:
        player.move_right(PLAYER_VEL)

    # Handle player collisions with other game objects
    # handle_horizontal_collision(player, objects)
    handle_vertical_collision(player, objects, player.y_vel)


# Function to handle horizontal collisions (currently empty)
def collide (player, objects, dx):
    player.move(dx, 0)
    player.update()
    collided_obj = None
    for obj in objects:
        if pygame.sprite.collide_rect(obj, player):
            collided_obj = obj
            break

    player.move(-dx, 0)
    player.update()
    return collided_obj


# The main function that drives the game
def main():
    running = True  # Boolean variable to keep track of the game state
    block_size = 64  # Size of the game objects
    player = Player(100, 64, block_size, block_size)  # Create a player instance

    # Connect to the server
    threads = connect(player)

    # Create the floor for the game
    floor = [Block(i * block_size, HEIGHT - block_size, block_size) for i in
             range(-WIDTH // block_size, WIDTH * 2 // block_size)]  # List comprehension to create the floor

    # List of game objects
    objects = [*floor, Block(0, HEIGHT - block_size * 2, block_size)]

    while running:
        clock.tick(FPS)

        # Event handling for game events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # If the user closes the game window
                running = False  # Set the game state to false
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.jump(objects=objects)  # Call the jump function if the user presses the spacebar

        player.loop(FPS)  # Call the loop function to update the player's position
        handle_movement(player, objects)  # Call the handle_movement function to handle player movements
        draw(win=screen, other_players=online_players,
             objects=objects)  # Call the draw function to draw the game objects

    pygame.quit()


# Ensure that the main game logic only runs if the script is run directly (as opposed to being imported as a module)
if __name__ == "__main__":
    main()
