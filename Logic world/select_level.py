from button import *
from input_manager import *
from image_factory import get_image
from world import World
import pygame
pygame.init()

def inv_bt_get_image(w, h, type, color, text=None):
    img = pygame.Surface((w, h), flags=pygame.SRCALPHA)
    img.fill(color)
    pygame.draw.rect(img, (50, 50, 50), (w * 0.1, h * 0.1, w * 0.8, h * 0.8))
    if (text != None):
        img.blit(text, (0, 0))
    return(img)
def dark_inv_bt_get_image(w, h, type, color, text=None):
    img = pygame.Surface((w, h), flags=pygame.SRCALPHA)
    img.fill(color)
    pygame.draw.rect(img, (50, 50, 50), (w * 0.1, h * 0.1, w * 0.8, h * 0.8))
    if (text != None):
        img.blit(text, (0, 0))
    dark = pygame.Surface((w, h), flags=pygame.SRCALPHA)
    dark.fill((0, 0, 0, 128))
    img.blit(dark, (0, 0))
    return(img)

def change_level(main, num):
    main.menu = World(main, w=10, h=10, block_scale=40, is_creative=0, number=num)
    main.menu.load_level("game_levels/level" + str(num))

class SelectLevel():
    def __init__(self, main):
        self.input_manager = input_manager
        self.main = main
        W = pygame.display.Info().current_w
        H = pygame.display.Info().current_h
        self.floor_img = pygame.Surface((W, H))
        for x in range(int(W / 40)):
            for y in range(int(H / 40)):
                self.floor_img.blit(get_image(1, 0), (x * 40, y * 40))
        #
        file = open("files/save.dat")
        txt = file.readline()
        file.close()
        #
        self.max_level = int(txt)
        #
        self.buttons = []
        for i in range(7):
            if i <= self.max_level + 1:
                self.buttons.append(get_button(80 + 120 * i, 80, 80, 80, str(i + 1), onrelease=change_level,
                                               onrelease_params=[self.main, i], get_bt_img=inv_bt_get_image,
                                               font_size=50, color1=(20, 20, 20), color2=(40, 40, 40), color3=(40, 40, 40)))
            else:
                self.buttons.append(get_button(80 + 120 * i, 80, 80, 80, str(i + 1), get_bt_img=dark_inv_bt_get_image,
                                               font_size=50, color1=(20, 20, 20), color2=(40, 40, 40), color3=(40, 40, 40)))

    def update(self, events):
        self.input_manager.update(events)
        #
        for b in self.buttons:
            b.update(events)
        #
        if self.input_manager.get_key("ESC"):
            from main_menu import MainMenu
            self.main.menu = MainMenu(self.main)

    def draw(self, screen):
        screen.blit(self.floor_img, (0, 0))
        for b in self.buttons:
            b.draw(screen)