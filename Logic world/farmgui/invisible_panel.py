from farmgui.component import *
import pygame
pygame.init()

class InvisiblePanel(Component):
    def __init__(self, rect, visible=1, **kwargs):
        Component.__init__(self, rect, kwargs.get("center"), visible=visible)
        self.buttons = []
        self.is_main = 0
        self.press_inv_button = 0

    def update_component(self, events):
        self.update(events)
        for b in self.buttons:
            if b.visible:
                b.update_component(events)

    def draw(self, screen):
        self.image.fill((0, 0, 0, 0))
        for b in self.buttons:
            if b.visible:
                b.draw(self.image)
        screen.blit(self.image, (0, 0))

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

    def get_components(self):
        return(self.buttons)

    def is_panel(self):
        return(1)