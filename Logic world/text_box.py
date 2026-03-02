from input_manager import *
from image_factory import *
import pygame
pygame.init()

class TextBox():
    def __init__(self, pos, inactive_image, hover_image,
                 text="",
                 font=None,
                 font_name="times new roman",
                 font_size=40,
                 font_color=(0, 0, 0),
                 font_alpha=True,
                 text_x=10,
                 **kwargs):
        self.pos = pos
        self.input_manager = input_manager
        self.text = text
        self.inactive_image = inactive_image
        self.hover_image = hover_image
        self.image = inactive_image
        self.rect = self.image.get_rect()
        self.mouselast = 0
        self.size = font_size
        self.color = font_color
        if font == None: font = pygame.font.SysFont(font_name, font_size)
        self.font = font
        self.font_alpha = font_alpha
        self.text_x = text_x
        self.timer = 0

    def update(self, events):
        self.timer += 1
        self.timer %= 60
        mousedown = pygame.mouse.get_pressed()[0]
        mousepos = pygame.mouse.get_pos()
        mouse_collide = (mousepos[0] >= self.pos[0] and mousepos[0] <= self.pos[0] + self.rect.w) and (mousepos[1] >= self.pos[1] and mousepos[1] <= self.pos[1] + self.rect.h)
        if mouse_collide:
            if mousedown:
                if self.input_manager.mousetag_object[0] == None:
                    self.input_manager.mousetag_object[0] = self
            else:
                if self.input_manager.mousetag_object[0] == self:
                    self.input_manager.mousetag_object[0] = None
                self.image = self.hover_image
                if self.mouselast:
                    self.input_manager.mouse_connect_object[0] = self
            self.mouselast = mousedown
        else:
            if self.input_manager.mousetag_object[0] == self:
                self.input_manager.mouse_connect_object[0] = self
                if not mousedown:
                    self.input_manager.mousetag_object[0] = None
            if not mousedown:
                self.image = self.inactive_image
            if mousedown and self.input_manager.mouse_connect_object[0] == self:
                self.input_manager.mouse_connect_object[0] = None
        if self.input_manager.mouse_connect_object[0] == self:
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        self.text = self.text[:len(self.text) - 1]
                    else:
                        text_img = self.font.render(self.text + event.unicode, True, self.color)
                        if text_img.get_width() < self.rect.w - self.text_x:
                            self.text = self.text + event.unicode

    def draw(self, screen):
        screen.blit(self.image, self.pos)
        render_text(self.text, (self.pos[0] + self.text_x, self.pos[1] + self.rect.h / 2), screen, centery="center", font=self.font, color=self.color, font_alpha=self.font_alpha)
        if self.timer < 30 and self.input_manager.mouse_connect_object[0] == self:
            text_img = self.font.render(self.text, self.font_alpha, self.color)
            pygame.draw.rect(screen, self.color, (self.pos[0] + self.text_x + text_img.get_width(), self.pos[1] + self.rect.h / 2 - text_img.get_height() / 2, 2, text_img.get_height()))

def get_text_box(x, y, w, h, text, size=40, color=(0, 0, 0), text_x=10, **kwargs):
    text_box = TextBox((x, y), get_text_box_image(w, h, (90, 90, 90)), get_text_box_image(w, h, (120, 120, 120)), font=kwargs.get("font"),
                       size=size, color=color, text_x=text_x, font_alpha=False)
    text_box.text = text
    return(text_box)