from block import Block
from button import Button
from client import *
from server import Server
from textInputBox import *

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


# Function to draw the game objects on the game window
def draw(win, other_players, objects):
    SCREEN.fill("white")  # Fill the game screen with white color

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
    player = Player(64, 64, block_size, block_size)  # Create a player instance

    # Connect to the server
    if ip_client:
        client = Client(ip_client)
    else:
        client = Client(ip_server)
    client.connect(player, ip_server)

    # Create the floor for the game
    floor = [Block(i * block_size, HEIGHT - block_size, block_size) for i in
             range(-WIDTH // block_size, WIDTH * 2 // block_size)]  # List comprehension to create the floor

    # List of game objects
    objects = [*floor, Block(0, HEIGHT - block_size * 2, block_size), Block(WIDTH-block_size, HEIGHT - block_size * 2, block_size)]

    while running:
        CLOCK.tick(FPS)

        # Event handling for game events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # If the user closes the game window
                running = False  # Set the game state to false
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.jump(objects=objects)  # Call the jump function if the user presses the spacebar

        player.loop(FPS)  # Call the loop function to update the player's position
        handle_movement(player, objects)  # Call the handle_movement function to handle player movements
        draw(win=SCREEN, other_players=client.online_players,
             objects=objects)  # Call the draw function to draw the game objects

    pygame.quit()


def start_server(ip):
    server = Server(ip)
    thread_server = threading.Thread(target=server.start)
    thread_server.start()


def create():
    while True:
        MENU_TEXT = get_font(100).render("CREATE GAME", True, "#ffffff")
        MENU_RECT = MENU_TEXT.get_rect(center=(WIDTH / 2, 100))

        SUBMIT_BUTTON = Button(image=pygame.image.load("assets/image.png"), pos=(WIDTH / 2, 250),
                               text_input="submit", font=get_font(75), base_color="#ffffff", hovering_color="#FF69B4")

        BACK_BUTTON = Button(image=pygame.image.load("assets/image.png"), pos=(WIDTH / 2, 500),
                             text_input="back", font=get_font(75), base_color="#ffffff", hovering_color="#FF69B4")

        INPUT_BOX = TextInputBox((WIDTH / 2), 375, 381, get_font(75), "#ffffff")
        GROUP = pygame.sprite.Group(INPUT_BOX)
        SCREEN.fill("black")

        running = True
        while running:
            SCREEN.fill("black")
            CLOCK.tick(FPS)
            MENU_MOUSE_POS = pygame.mouse.get_pos()

            events = pygame.event.get()
            GROUP.update(events)

            for button in [BACK_BUTTON, SUBMIT_BUTTON]:
                button.change_color(MENU_MOUSE_POS)
                button.update(SCREEN)

            # Event handling for game events
            for event in events:
                if event.type == pygame.QUIT:  # If the user closes the game window
                    pygame.quit()  # Quit the game
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if BACK_BUTTON.check_for_input(MENU_MOUSE_POS):
                        running = False
                        main()

                    if SUBMIT_BUTTON.check_for_input(MENU_MOUSE_POS):
                        running = False
                        start_server(INPUT_BOX.text)
                        game(INPUT_BOX.text)

            SCREEN.blit(MENU_TEXT, MENU_RECT)
            GROUP.draw(SCREEN)
            pygame.display.update()


def join():
    while True:
        MENU_TEXT = get_font(100).render("JOIN GAME", True, "#ffffff")
        MENU_RECT = MENU_TEXT.get_rect(center=(WIDTH / 2, 100))

        SUBMIT_BUTTON = Button(image=pygame.image.load("assets/image.png"), pos=(WIDTH / 2, 250),
                               text_input="submit", font=get_font(75), base_color="#ffffff", hovering_color="#FF69B4")

        BACK_BUTTON = Button(image=pygame.image.load("assets/image.png"), pos=(WIDTH / 2, 625),
                             text_input="back", font=get_font(75), base_color="#ffffff", hovering_color="#FF69B4")

        INPUT_BOX_SERVER = TextInputBox((WIDTH / 2), 375, 381, get_font(75), "#ffffff")
        INPUT_BOX_CLIENT = TextInputBox((WIDTH / 2), 500, 381, get_font(75), "#ffffff")
        GROUP_SERVER = pygame.sprite.Group(INPUT_BOX_SERVER)
        GROUP_CLIENT = pygame.sprite.Group(INPUT_BOX_CLIENT)
        SCREEN.fill("black")

        running = True
        while running:
            SCREEN.fill("black")
            CLOCK.tick(FPS)
            MENU_MOUSE_POS = pygame.mouse.get_pos()

            events = pygame.event.get()
            GROUP_SERVER.update(events)
            GROUP_CLIENT.update(events)

            for button in [BACK_BUTTON, SUBMIT_BUTTON]:
                button.change_color(MENU_MOUSE_POS)
                button.update(SCREEN)

            # Event handling for game events
            for event in events:
                if event.type == pygame.QUIT:  # If the user closes the game window
                    pygame.quit()  # Quit the game
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if BACK_BUTTON.check_for_input(MENU_MOUSE_POS):
                        running = False
                        main()

                    if SUBMIT_BUTTON.check_for_input(MENU_MOUSE_POS):
                        running = False
                        game(ip_server=INPUT_BOX_SERVER.text, ip_client=INPUT_BOX_CLIENT.text)

            SCREEN.blit(MENU_TEXT, MENU_RECT)
            GROUP_SERVER.draw(SCREEN)
            GROUP_CLIENT.draw(SCREEN)
            pygame.display.update()


def main():
    MENU_TEXT = get_font(100).render("HELNA", True, "#ffffff")
    MENU_RECT = MENU_TEXT.get_rect(center=(WIDTH / 2, 100))

    CREATE_BUTTON = Button(image=pygame.image.load("assets/image.png"), pos=(WIDTH / 2, 250),
                           text_input="create", font=get_font(75), base_color="#ffffff", hovering_color="#FF69B4")
    JOIN_BUTTON = Button(image=pygame.image.load("assets/image.png"), pos=(WIDTH / 2, 375),
                         text_input="join", font=get_font(75), base_color="#ffffff", hovering_color="#FF69B4")
    QUIT_BUTTON = Button(image=pygame.image.load("assets/image.png"), pos=(WIDTH / 2, 500),
                         text_input="quit", font=get_font(75), base_color="#ffffff", hovering_color="#FF69B4")

    SCREEN.fill("black")
    SCREEN.blit(MENU_TEXT, MENU_RECT)

    running = True  # Boolean variable to keep track of the game state

    while running:
        CLOCK.tick(FPS)
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        for button in [CREATE_BUTTON, JOIN_BUTTON, QUIT_BUTTON]:
            button.change_color(MENU_MOUSE_POS)
            button.update(SCREEN)

        # Event handling for game events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # If the user closes the game window
                pygame.quit()  # Quit the game
            if event.type == pygame.MOUSEBUTTONDOWN:
                if CREATE_BUTTON.check_for_input(MENU_MOUSE_POS):
                    running = False
                    create()
                if JOIN_BUTTON.check_for_input(MENU_MOUSE_POS):
                    join()
                    running = False
                if QUIT_BUTTON.check_for_input(MENU_MOUSE_POS):
                    pygame.quit()

        pygame.display.update()
    pygame.quit()


# Ensure that the main game logic only runs if the script is run directly (as opposed to being imported as a module)
if __name__ == "__main__":
    main()
