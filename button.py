class Button():
    def __init__(self, image, pos, text_input, font, base_color, hovering_color):
        """
        Initialize Button attributes.

        Args:
            image (pygame.Surface): The image to display on the button.
            pos (tuple): The position of the button.
            text_input (str): The text to display on the button.
            font (pygame.font.Font): The font used for rendering text.
            base_color (str): The base color of the text.
            hovering_color (str): The color of the text when hovering.
        """
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
        """
        Update the button on the screen.

        Args:
            screen (pygame.Surface): The surface to blit the button onto.
        """
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def check_for_input(self, position):
        """
        Check if the given position is within the button.

        Args:
            position (tuple): The position to check.

        Returns:
            bool: True if the position is within the button, False otherwise.
        """
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False

    def change_color(self, position):
        """
        Change the color of the button text based on hovering.

        Args:
            position (tuple): The position of the mouse cursor.
        """
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)
