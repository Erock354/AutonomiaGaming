import pygame

from block import Block
from button import Button
from client import *
from server import Server
from textInputBox import *
from player import *

# Initialize pygame and set a title for the window
pygame.init()
pygame.display.set_caption("")

# Define some global constants like HEIGHT, WIDTH, PLAYER_VEL (player_velocity), FPS (frames_per_second), clock (used
# for setting game clock), and screen (main game window)
HEIGHT = 720
WIDTH = 1280
PLAYER_VEL = 8
FPS = 120
CLOCK = pygame.time.Clock()
SCREEN = pygame.display.set_mode([WIDTH, HEIGHT])
SURFACE = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)


# Function to draw the game objects on the game window
def draw(other_players, objects, bullets):
    SCREEN.fill("white")  # Fill the game screen with white color
    SCREEN.blit(SURFACE, (0, 0))
    SURFACE.fill((0, 0, 0, 0))  # Reset surface

    # Draw the static game objects 
    for obj in objects:
        obj.draw(SCREEN)

    # Draw the online players on the screen
    for player in other_players:
        player.draw(SURFACE)

    for bullet in bullets:
        bullet.draw(SCREEN)

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
def collide(player, objects, dx):
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


def get_font(size):  # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)


# The main function that drives the game
def game(ip_server, ip_client=None):
    running = True  # Boolean variable to keep track of the game state
    block_size = 64  # Size of the game objects
    player = Player(64, HEIGHT-64, block_size, block_size, (255, 0, 0))  # Create a player instance
    # Connect to the server
    if ip_client:
        client = Client(player, ip_server, ip_client)
    else:
        client = Client(player, ip_server, ip_server)
    client.connect()

    # Create the floor for the game
    floor = [Block(i * block_size, HEIGHT - block_size, block_size) for i in
             range(-WIDTH // block_size, WIDTH * 2 // block_size)]  # List comprehension to create the floor

    # List of game objects
    objects = [*floor, Block(0, HEIGHT - block_size * 2, block_size),
               Block(WIDTH - block_size, HEIGHT - block_size * 2, block_size)]

    while running:
        CLOCK.tick(FPS)
        # Event handling for game events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # If the user closes the game window
                running = False  # Set the game state to false
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.jump(objects=objects)  # Call the jump function if the user presses the space bar

            if pygame.mouse.get_pressed() == (1, 0, 0):  # Shoot when mouse left click
                player.shoot(client)

        for bullet in client.bullets:
            bullet.update(SCREEN)
            if bullet.rect.x < 0 or bullet.rect.x > SCREEN.get_width() or bullet.rect.y < 0 or bullet.rect.y > SCREEN.get_height():
                client.bullets.remove(bullet)

            if pygame.rect.Rect.colliderect(bullet.rect, player):
                player.hp = player.hp - 2.5
                if player.hp < 0:
                    player.hp = 0

        player.loop(FPS)  # Call the loop function to update the player's position
        handle_movement(player, objects)  # Call the handle_movement function to handle player movements
        draw(other_players=client.online_players, objects=objects, bullets=client.bullets)  # Call the draw function to draw the game objects

    pygame.quit()


def start_server(ip):
    server = Server(ip)
    thread_server = threading.Thread(target=server.start)
    thread_server.start()


def create():
    # Render title for the menu
    MENU_TEXT = get_font(100).render("CREATE GAME", True, "#ffffff")
    MENU_RECT = MENU_TEXT.get_rect(center=(WIDTH / 2, 100))

    # Create buttons for submit and back actions
    SUBMIT_BUTTON = Button(image=pygame.image.load("assets/image.png"), pos=(WIDTH / 2, 250),
                           text_input="submit", font=get_font(75), base_color="#ffffff", hovering_color="#FF69B4")

    # Create input boxes for server and client IP addresses
    BACK_BUTTON = Button(image=pygame.image.load("assets/image.png"), pos=(WIDTH / 2, 500),
                         text_input="back", font=get_font(75), base_color="#ffffff", hovering_color="#FF69B4")

    # Create input boxes for server and client IP addresses
    INPUT_BOX = TextInputBox((WIDTH / 2), 375, 381, get_font(75), "#ffffff", "host ip")
    GROUP = pygame.sprite.Group(INPUT_BOX)  # Sprite group to manage the input box

    running = True
    while running:  # Loop for handling events and updating display
        SCREEN.fill("black")
        CLOCK.tick(FPS)
        # Getting the current mouse position
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        # Handling events for the input box
        events = pygame.event.get()
        GROUP.update(events)

        # Updating the colors and appearance of buttons based on mouse position
        for button in [BACK_BUTTON, SUBMIT_BUTTON]:
            button.change_color(MENU_MOUSE_POS)
            button.update(SCREEN)

        # Event handling for game events
        for event in events:
            # Quitting the game if the user closes the game window
            if event.type == pygame.QUIT:
                pygame.quit()
            # Handling mouse button clicks
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Checking if the back button is clicked
                if BACK_BUTTON.check_for_input(MENU_MOUSE_POS):
                    # Exiting the 'create' function and returning to the main menu
                    running = False
                    main()

                # Checking if the submit button is clicked
                if SUBMIT_BUTTON.check_for_input(MENU_MOUSE_POS):
                    # Exiting the 'create' function and starting the server
                    # and the game with the input box text as an argument
                    running = False
                    start_server(INPUT_BOX.text)
                    game(INPUT_BOX.text)

        SCREEN.blit(MENU_TEXT, MENU_RECT)  # Draw menu text
        GROUP.draw(SCREEN)  # Draw client input box
        pygame.display.update()  # Update display


def join():
    while True:  # Continuous loop until an action breaks it
        # Render title for the menu
        MENU_TEXT = get_font(100).render("JOIN GAME", True, "#ffffff")
        MENU_RECT = MENU_TEXT.get_rect(center=(WIDTH / 2, 100))

        # Create buttons for submit and back actions
        SUBMIT_BUTTON = Button(image=pygame.image.load("assets/image.png"), pos=(WIDTH / 2, 250),
                               text_input="submit", font=get_font(75), base_color="#ffffff", hovering_color="#FF69B4")
        BACK_BUTTON = Button(image=pygame.image.load("assets/image.png"), pos=(WIDTH / 2, 625),
                             text_input="back", font=get_font(75), base_color="#ffffff", hovering_color="#FF69B4")

        # Create input boxes for server and client IP addresses
        INPUT_BOX_SERVER = TextInputBox((WIDTH / 2), 375, 381, get_font(75), "#ffffff", "host ip")
        INPUT_BOX_CLIENT = TextInputBox((WIDTH / 2), 500, 381, get_font(75), "#ffffff", "client ip")
        GROUP_SERVER = pygame.sprite.Group(INPUT_BOX_SERVER)  # Group for server input box
        GROUP_CLIENT = pygame.sprite.Group(INPUT_BOX_CLIENT)  # Group for client input box
        SCREEN.fill("black")  # Clear the screen

        running = True
        while running:  # Loop for handling events and updating display
            SCREEN.fill("black")  # Clear the screen
            CLOCK.tick(FPS)  # Limit frame rate
            MENU_MOUSE_POS = pygame.mouse.get_pos()  # Get mouse position

            events = pygame.event.get()  # Get all events
            GROUP_SERVER.update(events)  # Update server input box
            GROUP_CLIENT.update(events)  # Update client input box

            for button in [BACK_BUTTON, SUBMIT_BUTTON]:
                button.change_color(MENU_MOUSE_POS)  # Change button color if mouse hovers over it
                button.update(SCREEN)  # Update button on the screen

            # Event handling for game events
            for event in events:
                if event.type == pygame.QUIT:  # If the user closes the game window
                    pygame.quit()  # Quit the game
                if event.type == pygame.MOUSEBUTTONDOWN:  # If mouse button is clicked
                    if BACK_BUTTON.check_for_input(MENU_MOUSE_POS):  # If back button is clicked
                        running = False  # Stop the loop
                        main()  # Go back to the main menu

                    if SUBMIT_BUTTON.check_for_input(MENU_MOUSE_POS):  # If submit button is clicked
                        running = False  # Stop the loop
                        game(ip_server=INPUT_BOX_SERVER.text, ip_client=INPUT_BOX_CLIENT.text)  # Start the game

            SCREEN.blit(MENU_TEXT, MENU_RECT)  # Draw menu text
            GROUP_SERVER.draw(SCREEN)  # Draw server input box
            GROUP_CLIENT.draw(SCREEN)  # Draw client input box
            pygame.display.update()  # Update display


def main():
    # Render title for the menu
    MENU_TEXT = get_font(100).render("HELNA", True, "#ffffff")
    MENU_RECT = MENU_TEXT.get_rect(center=(WIDTH / 2, 100))

    # Create buttons for redirect to the other pages
    CREATE_BUTTON = Button(image=pygame.image.load("assets/image.png"), pos=(WIDTH / 2, 250),
                           text_input="create", font=get_font(75), base_color="#ffffff", hovering_color="#FF69B4")
    JOIN_BUTTON = Button(image=pygame.image.load("assets/image.png"), pos=(WIDTH / 2, 375),
                         text_input="join", font=get_font(75), base_color="#ffffff", hovering_color="#FF69B4")
    QUIT_BUTTON = Button(image=pygame.image.load("assets/image.png"), pos=(WIDTH / 2, 500),
                         text_input="quit", font=get_font(75), base_color="#ffffff", hovering_color="#FF69B4")
    SCREEN.fill("black")  # Clear the screen
    SCREEN.blit(MENU_TEXT, MENU_RECT)  # Draw the title

    running = True  # Boolean variable to keep track of the game state

    while running:
        CLOCK.tick(FPS)
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        for button in [CREATE_BUTTON, JOIN_BUTTON, QUIT_BUTTON]:
            button.change_color(MENU_MOUSE_POS)
            button.update(SCREEN)

        # Event handling for game events
        for event in pygame.event.get():  # Iterate through all events in the Pygame event queue
            if event.type == pygame.QUIT:  # If the user closes the game window
                pygame.quit()  # Quit the game

            if event.type == pygame.MOUSEBUTTONDOWN:  # If a mouse button is pressed
                if CREATE_BUTTON.check_for_input(
                        MENU_MOUSE_POS):  # Check if the mouse click is within the bounds of the CREATE_BUTTON
                    create()  # Opens the create game menu
                    running = False  # Stop the game loop

                if JOIN_BUTTON.check_for_input(
                        MENU_MOUSE_POS):  # Check if the mouse click is within the bounds of the JOIN_BUTTON
                    join()  # Opens the join game menu
                    running = False  # Stop the game loop

                if QUIT_BUTTON.check_for_input(
                        MENU_MOUSE_POS):  # Check if the mouse click is within the bounds of the QUIT_BUTTON
                    pygame.quit()  # Quit the game

        pygame.display.update()
    pygame.quit()


# Ensure that the main game logic only runs if the script is run directly (as opposed to being imported as a module)
if __name__ == "__main__":
    main()
