from image_factory import *
import pygame
pygame.init()

class Button():
    def __init__(self, pos, IM, inactive_image, pressed_image, hover_image, **kwargs):
        self.input_manager = IM
        self.pos = pos
        self.inactive_image = inactive_image
        self.pressed_image = pressed_image
        self.hover_image = hover_image
        self.image = self.inactive_image
        self.rect = self.image.get_rect()
        self.onclick = kwargs.get("onclick")
        self.onclick_params = kwargs.get("onclick_params")
        self.onrelease = kwargs.get("onrelease")
        self.onrelease_params = kwargs.get("onrelease_params")

    def update(self, events):
        mousedown = pygame.mouse.get_pressed()[0]
        mousepos = pygame.mouse.get_pos()
        mouse_collide = (mousepos[0] >= self.pos[0] and mousepos[0] <= self.pos[0] + self.rect.w) and (mousepos[1] >= self.pos[1] and mousepos[1] <= self.pos[1] + self.rect.h)
        if mouse_collide:
            if mousedown:
                if self.input_manager.mousetag_object[0] == None:
                    self.input_manager.mousetag_object[0] = self
                    self.image = self.pressed_image
                    if str(type(self.onclick)) == "<class 'function'>":
                        if self.onclick_params != None:
                            self.onclick(*self.onclick_params)
                        else:
                            self.onclick()
            else:
                if self.input_manager.mousetag_object[0] == self:
                    if str(type(self.onrelease)) == "<class 'function'>":
                        if self.onrelease_params != None:
                            self.onrelease(*self.onrelease_params)
                        else:
                            self.onrelease()
                    self.input_manager.mousetag_object[0] = None
                self.image = self.hover_image
        else:
            if self.input_manager.mousetag_object[0] == self:
                self.image = self.pressed_image
            if not mousedown:
                if self.input_manager.mousetag_object[0] == self:
                    if str(type(self.onrelease)) == "<class 'function'>":
                        if self.onrelease_params != None:
                            self.onrelease(*self.onrelease_params)
                        else:
                            self.onrelease()
                    self.input_manager.mousetag_object[0] = None
                self.image = self.inactive_image

    def draw(self, screen):
        screen.blit(self.image, self.pos)

def get_button(x, y, w, h, text, input_manager, font_size=70, text_color=(0, 0, 0), **kwargs):
    alpha = kwargs.get("alpha")
    if alpha == None:
        alpha = 0
    t = render_text(text, (w * 40 / 2, h * 40 / 2), w * 40, h * 40, centerx="center", centery="center", font=pygame.font.Font("files/faithful.ttf", font_size), alpha=alpha, color=text_color)
    b = Button((x, y), input_manager, get_button_image(w, h, 0, text=t), get_button_image(w, h, 2, text=t), get_button_image(w, h, 1, text=t), onclick=kwargs.get("onclick"), onclick_params=kwargs.get("onclick_params"), onrelease=kwargs.get("onrelease"), onrelease_params=kwargs.get("onrelease_params"))
    return(b)