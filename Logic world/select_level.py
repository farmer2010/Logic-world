from button import *
from input_manager import *
from image_factory import get_image
from world import World
import pygame
pygame.init()

def change_level(main, num):
    main.menu = World(main, w=10, h=10, block_scale=40)
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
        self.buttons = []
        for i in range(7):
            self.buttons.append(get_button(80 + 120 * i, 80, 80, 80, str(i + 1), onrelease=change_level, onrelease_params=[self.main, i]))

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