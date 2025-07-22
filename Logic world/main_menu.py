import pygame
pygame.init()
from input_manager import InputManager
from button import *
from image_factory import *
from world import World
from ui import UI


def editor(main):
    W = pygame.display.Info().current_w
    H = pygame.display.Info().current_h
    b = 40
    main.menu = World(main, w=int(W / b), h=int(H / b), pos=[0, 0], block_scale=b)

class MainMenu():
    def __init__(self, main):
        self.main = main
        self.input_manager = InputManager()
        W = pygame.display.Info().current_w
        H = pygame.display.Info().current_h
        self.floor_img = pygame.Surface((W, H))
        self.floor_img.fill((30, 30, 30))
        for x in range(int(W / 40)):
            for y in range(int(H / 40)):
                    self.floor_img.blit(get_image(1, 0), (x * 40, y * 40))
        self.buttons = []
        self.buttons.append(get_button(720, 450, 12, 3, "PLAY", self.input_manager, font_size=90))
        self.buttons.append(get_button(720, 600, 12, 3, "EDITOR", self.input_manager, font_size=90, onrelease=editor, onrelease_params=[self.main]))
        self.buttons.append(get_button(720, 750, 12, 3, "SETTINGS", self.input_manager, font_size=90))

    def update(self, events):
        #self.input_manager.update(events)
        for b in self.buttons:
            b.update(events)

    def draw(self, screen):
        screen.blit(self.floor_img, (0, 0))
        for b in self.buttons:
            b.draw(screen)