import pygame


class TextInputBox(pygame.sprite.Sprite):
    def __init__(self, x, y, w, font, color):
        """
        Initialize TextInputBox attributes.

        Args:
            x (int): The x-coordinate of the box.
            y (int): The y-coordinate of the box.
            w (int): The width of the box.
            font (pygame.font.Font): The font used for rendering text.
            color (str): The color of the text.
        """
        super().__init__()
        self.color = color
        self.backcolor = "black"  # Background color of the text box
        self.boxcolor = "#2C2F33"  # Border color of the text box
        self.pos = (x, y)  # Position of the text box
        self.width = w  # Width of the text box
        self.font = font  # Font used for rendering text
        self.active = False  # Flag to indicate if the text box is active
        self.text = ""  # Text entered into the text box
        self.render_text()  # Render the initial text

    def render_text(self):
        """
        Render the text onto the text box surface.
        """
        # Render the text surface
        t_surf = self.font.render(self.text, True, self.color, self.backcolor)
        # Create a surface for the text box
        self.image = pygame.Surface((max(self.width, t_surf.get_width()), t_surf.get_height()), pygame.SRCALPHA)
        # Blit the text onto the text box surface
        self.image.blit(t_surf, (0, 0))
        # Draw the border of the text box
        pygame.draw.rect(self.image, self.boxcolor, self.image.get_rect(), 2)
        # Set the position of the text box
        self.rect = self.image.get_rect(center=self.pos)

    def update(self, event_list):
        """
        Update the text box based on the given event list.

        Args:
            event_list (list): A list of pygame events.
        """
        # Iterate through the list of events
        for event in event_list:
            # Check for mouse button press event and if the text box is not active
            if event.type == pygame.MOUSEBUTTONDOWN and not self.active:
                # Activate the text box if the mouse click is within the text box boundary
                self.active = self.rect.collidepoint(event.pos)
            # Check for keyboard key press event and if the text box is active
            if event.type == pygame.KEYDOWN and self.active:
                # Handle key presses
                if event.key == pygame.K_RETURN:
                    # Deactivate the text box on pressing Enter
                    self.active = False
                elif event.key == pygame.K_BACKSPACE:
                    # Remove the last character from the text on pressing Backspace
                    self.text = self.text[:-1]
                else:
                    # Add the character corresponding to the key press to the text
                    self.text += event.unicode
                # Re-render the text box with the updated text
                self.render_text()
