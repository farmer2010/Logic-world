from utils import *
from image_factory import *
import pygame
pygame.init()

class TextBox():
    def __init__(self, pos, input_manager, inactive_image, hover_image, **kwargs):
        self.pos = pos
        self.input_manager = input_manager
        self.text = ""
        self.inactive_image = inactive_image
        self.hover_image = hover_image
        self.image = inactive_image
        self.rect = self.image.get_rect()
        self.mouselast = 0
        self.size = kwargs.get("size")
        if self.size == None:
            self.size = 40
        self.color = kwargs.get("color")
        if self.color == None:
            self.color = (0, 0, 0)
        self.font = kwargs.get("font")
        if self.font == None:
            self.font = pygame.font.SysFont(None, self.size)
        self.text_x = kwargs.get("text_x")
        if self.text_x == None:
            self.text_x = 10
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
        render_text(self.text, (self.pos[0] + self.text_x, self.pos[1] + self.rect.h / 2), screen, centery="center", font=self.font, color=self.color)
        if self.timer < 30 and self.input_manager.mouse_connect_object[0] == self:
            text_img = self.font.render(self.text, True, self.color)
            pygame.draw.rect(screen, self.color, (self.pos[0] + self.text_x + text_img.get_width(), self.pos[1] + self.rect.h / 2 - text_img.get_height() / 2, 4, text_img.get_height()))

def get_text_box(x, y, w, h, text, input_manager, **kwargs):
    text_box = TextBox((x, y), input_manager, get_button_image(w, h, 4), get_button_image(w, h, 5), font=kwargs.get("font"), size=kwargs.get("size"), color=kwargs.get("color"), text_x=kwargs.get("text_x"))
    text_box.text = text
    return(text_box)