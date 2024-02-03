import pygame


class TextInputBox(pygame.sprite.Sprite):
    def __init__(self, x, y, w, font, color):
        super().__init__()
        self.color = color
        self.backcolor = "black"
        self.boxcolor = "#2C2F33"
        self.pos = (x, y)
        self.width = w
        self.font = font
        self.active = False
        self.text = ""
        self.render_text()

    def render_text(self):
        t_surf = self.font.render(self.text, True, self.color, self.backcolor)
        self.image = pygame.Surface((max(self.width, t_surf.get_width()), t_surf.get_height()), pygame.SRCALPHA)
        self.image.blit(t_surf, (0, 0))
        pygame.draw.rect(self.image, self.boxcolor, self.image.get_rect(), 2)
        self.rect = self.image.get_rect(center=self.pos)

    def update(self, event_list):
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN and not self.active:
                self.active = self.rect.collidepoint(event.pos)
            if event.type == pygame.KEYDOWN and self.active:
                if event.key == pygame.K_RETURN:
                    self.active = False
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.render_text()
