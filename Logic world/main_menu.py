#from world import World
from select_level import SelectLevel
from farmgui.gui import *
from blocks.image_factory import *
import pygame
pygame.init()

W = pygame.display.Info().current_w
H = pygame.display.Info().current_h
font60=pygame.font.Font("files/Better VCR 6.1.ttf", 60)

def editor(self):
    self.visible = 0
    self.parent.get_component(2).set_visible(2)
def play(self):
    self.visible = 0
    self.parent.get_component(1).set_visible(1)
def quit(main):
    main.keep_going = 0

class MainMenu(Panel):
    def __init__(self, rect, visible=1):
        Panel.__init__(self, rect, visible=visible)
        for x in range(int(W / 40)):
            for y in range(int(H / 40)):
                    self.background_image.blit(get_image(1, 0), (x * 40, y * 40))
        #
        self.add(Button((720, 450, 480, 120), text="PLAY", font=font60, font_alpha=0, onrelease=play, onrelease_params=[self]))
        self.add(Button((720, 600, 480, 120), text="EDITOR", font=font60, font_alpha=0, onrelease=editor,onrelease_params=[self]))
        self.add(Button((720, 750, 480, 120), text="QUIT", font=font60, font_alpha=0, onrelease=quit,onrelease_params=[self]))

    def update(self, events):
        #
        #DRAW
        #
        screen = self.get_screen()