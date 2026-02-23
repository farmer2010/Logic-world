#настройка
from utils import *
import shutil
import pygame
from main_menu import MainMenu

pygame.init()
steps = 0

shutil.rmtree("__pycache__")
shutil.rmtree("blocks/__pycache__")

W = pygame.display.Info().current_w
H = pygame.display.Info().current_h
screen = pygame.display.set_mode([W, H])
pygame.display.set_caption("Logic world")
timer = pygame.time.Clock()

class Main():
    def __init__(self):
        self.menu = MainMenu(self)
        self.keep_going = True
game_world = Main()

while game_world.keep_going:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:#проверка выхода
            game_world.keep_going = False
    game_world.menu.draw(screen)
    game_world.menu.update(events)
    render_text(str(round(timer.get_fps(), 2)), (0, 0), screen, color=(255, 0, 0))
    pygame.display.update()
    timer.tick(30)
    steps += 1
pygame.quit()