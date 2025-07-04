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

    def update(self, events):
        mousedown = pygame.mouse.get_pressed()[0]
        mousepos = pygame.mouse.get_pos()
        mouse_collide = (mousepos[0] >= self.pos[0] and mousepos[0] <= self.pos[0] + self.rect.w) and (mousepos[1] >= self.pos[1] and mousepos[1] <= self.pos[1] + self.rect.h)
        if mouse_collide:
            if mousedown:
                if self.input_manager.mousetag[0] == 0:
                    self.input_manager.mousetag[0] = 1
                    self.input_manager.mousetag_object[0] = self
                    self.image = self.pressed_image
                    if str(type(self.onclick)) == "<class 'function'>":
                        if self.onclick_params != None:
                            self.onclick(self.onclick_params)
                        else:
                            self.onclick()
            else:
                self.input_manager.mousetag[0] = 0
                self.input_manager.mousetag_object[0] = None
                self.image = self.hover_image
        else:
            if  self.input_manager.mousetag_object[0] == self:
                self.image = self.pressed_image
            if not mousedown:
                self.input_manager.mousetag[0] = 0
                self.input_manager.mousetag_object[0] = None
                self.image = self.inactive_image

    def draw(self, screen):
        screen.blit(self.image, self.pos)