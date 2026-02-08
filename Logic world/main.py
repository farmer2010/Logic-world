#настройка
from farmgui.gui import *
import shutil
import pygame
from main_menu import MainMenu
from select_level import SelectLevel
from world import World

pygame.init()
steps = 0
keep_going = 1

shutil.rmtree("__pycache__")
shutil.rmtree("farmgui/__pycache__")
shutil.rmtree("blocks/__pycache__")

W = pygame.display.Info().current_w
H = pygame.display.Info().current_h
screen = pygame.display.set_mode([W, H])
pygame.display.set_caption("Logic world")
timer = pygame.time.Clock()
black = (0, 0, 0)

buttons = ButtonManager()

buttons.add(MainMenu((0, 0, 1920, 1080), visible=1))
buttons.add(SelectLevel((0, 0, 1920, 1080), visible=0))
buttons.add(World((0, 0, 1920, 1080), visible=0))

while keep_going:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:#проверка выхода
            keep_going = False
    buttons.update(screen, events)
    pygame.display.update()
    timer.tick(60)
    steps += 1
pygame.quit()