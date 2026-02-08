from farmgui.gui import *
from blocks.image_factory import *
import pygame
pygame.init()

W = pygame.display.Info().current_w
H = pygame.display.Info().current_h

class SelectLevel(Panel):
    def __init__(self, rect, visible=1):
        Panel.__init__(self, rect, visible=visible)
        for x in range(int(W / 40)):
            for y in range(int(H / 40)):
                self.background_image.blit(get_image(1, 0), (x * 40, y * 40))
        #

    def update(self, events):
        pass