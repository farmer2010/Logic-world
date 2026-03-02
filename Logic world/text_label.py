import pygame
pygame.init()

class TextLabel():
    def __init__(self, text, pos, font=None, font_name=None, font_size=30, font_color=(0, 0, 0), font_alpha=True, center=(0, 0)):
        if font == None: font = pygame.font.SysFont(font_name, font_size)
        self.center = center
        img = font.render(text, font_alpha, font_color)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.rect.x -= self.rect.w * self.center[0]
        self.rect.y -= self.rect.h * self.center[1]
        #
        self.font = font
        self.text = text
        self.font_color = font_color
        self.font_alpha = font_alpha
        self.update_text = None

    def add_update_text(self, upd):
        self.update_text = upd

    def set_text(self, text):
        self.text = text

    def update(self, events):
        if self.update_text != None:
            self.text = self.update_text()

    def draw(self, screen):
        self.image = self.font.render(self.text, self.font_alpha, self.font_color)
        screen.blit(self.image, self.rect)