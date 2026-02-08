from farmgui.utils import *
from farmgui.component import *
import pygame
pygame.init()

class Panel(Component):
    def __init__(self, rect, background_color=(50, 50, 50), is_main=0, visible=1, **kwargs):
        Component.__init__(self, rect, kwargs.get("center"), visible=visible)
        self.background_image = kwargs.get("background_image")
        if kwargs.get("background_image") == None:
            self.background_image = pygame.Surface((self.rect.w, self.rect.h), pygame.SRCALPHA)
            self.background_image.fill(background_color)
        self.inv_image = self.background_image = pygame.Surface((self.rect.w, self.rect.h), pygame.SRCALPHA)
        self.inv_image.fill((0, 0, 0, 0))
        self.buttons = []
        self.is_main = is_main

    def update_component(self, events):
        self.update(events)
        mousedown = pygame.mouse.get_pressed()[0]
        mouse_collide = self.collide()
        if mouse_collide:
            if mousedown:
                if self.input_manager.mousetag_object[0] == None:
                    press_button = 0
                    for b in self.buttons:
                        if b.visible:
                            m_c = b.collide()
                            press_button = m_c
                            if m_c:
                                break
                    if not press_button:
                        self.input_manager.mousetag_object[0] = self
            else:
                if self.input_manager.mousetag_object[0] == self:
                    self.input_manager.mousetag_object[0] = None
        else:
            if not mousedown:
                if self.input_manager.mousetag_object[0] == self:
                    self.input_manager.mousetag_object[0] = None
        for b in self.buttons:
            if b.visible:
                b.update_component(events)

    def draw(self, screen):
        self.image.blit(self.background_image, (0, 0))
        self.image.blit(self.inv_image, (0, 0))
        for b in self.buttons:
            if b.visible:
                b.draw(self.image)
        screen.blit(self.image, self.rect)
        self.inv_image.fill((0, 0, 0, 0))

    def add(self, b):
        self.buttons.append(b)
        b.parent = self
        if self.is_main:
            b.main = self
        else:
            b.main = self.main

    def remove(self, b):
        self.buttons.remove(b)

    def get_mousepos(self):
        mousepos = pygame.mouse.get_pos()
        if self.is_main == 0:
            mpos = (mousepos[0] - self.parent.rect.x, mousepos[1] - self.parent.rect.y)#позиция мыши относительно родительского компонента
            return(mpos)
        else:
            return(mousepos)

    def get_component(self, index):
        return(self.buttons[index])

    def get_component_count(self):
        return(len(self.buttons))

    def get_screen(self):
        return(self.inv_image)

    def is_panel(self):
        return(1)