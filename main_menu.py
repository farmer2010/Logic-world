import pygame
pygame.init()
from input_manager import InputManager
from button import Button
from image_factory import *
from ui import UI


def editor(main):
    W = pygame.display.Info().current_w
    H = pygame.display.Info().current_h
    main.menu = UI(main, [str(int(W / 40)), str(int(H / 40)), "0", "0", "1"])

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
        text = render_text("PLAY", (240, 60), 480, 120, centerx="center", centery="center", font=pygame.font.Font("files/font.ttf", 70), alpha=False)
        self.buttons.append(Button((720, 450), self.input_manager, get_button_image(12, 3, 0, text=text), get_button_image(12, 3, 2, text=text), get_button_image(12, 3, 1, text=text), onclick=lambda: print(1)))
        text = render_text("EDITOR", (240, 60), 480, 120, centerx="center", centery="center", font=pygame.font.Font("files/font.ttf", 70), alpha=False)
        self.buttons.append(Button((720, 600), self.input_manager, get_button_image(12, 3, 0, text=text), get_button_image(12, 3, 2, text=text), get_button_image(12, 3, 1, text=text), onclick=editor, onclick_params=(self.main)))
        text = render_text("OPTIONS", (240, 60), 480, 120, centerx="center", centery="center", font=pygame.font.Font("files/font.ttf", 70), alpha=False)
        self.buttons.append(Button((720, 750), self.input_manager, get_button_image(12, 3, 0, text=text), get_button_image(12, 3, 2, text=text), get_button_image(12, 3, 1, text=text), onclick=lambda: print(1)))

    def update(self, events):
        #self.input_manager.update(events)
        for b in self.buttons:
            b.update(events)

    def draw(self, screen):
        screen.blit(self.floor_img, (0, 0))
        for b in self.buttons:
            b.draw(screen)