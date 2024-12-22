#настройка
import pygame
from random import randint as rand
from world import World
from ui import UI
from select_level import SelectLevel as SL

pygame.init()
keep_going = True
steps = 0

W = pygame.display.Info().current_w
H = pygame.display.Info().current_h
screen = pygame.display.set_mode([W, H])
description = "Logic world"
pygame.display.set_caption(description)
timer = pygame.time.Clock()
black = (0, 0, 0)
menu = ["ui"]
last_menu = "ui"
#game_world = World(int(W / 40), int(H / 40))
#
data = [11, 11, 18, 8, "1"]
game_world = UI(menu, data)
#
#data = ["1"]
#game_world = SL(menu, data)

while keep_going:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:#проверка выхода
            keep_going = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:#-|-
                keep_going = False
    last_menu = menu[0]
    game_world.update(events)
    if last_menu != menu[0]:
        if menu[0] == "game":
            if last_menu == "ui":
                game_world = World(data[0], data[1], pos=[data[2], data[3]], level_name=data[4])
            elif lest_menu == "select_level":
                game_world = World(10, 10, pos=[0, 0], level_name=data[0])
                game_world.load_level("level" + data[0])
                game_world.is_creative = 0
    game_world.draw(screen)
    pygame.display.update()
    timer.tick(60)
    steps += 1
pygame.quit()
