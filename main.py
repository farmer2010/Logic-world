#настройка
import pygame
from random import randint as rand
import world

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
game_world = world.World(int(W / 40), int(H / 40))

while keep_going:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:#проверка выхода
            keep_going = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:#-|-
                keep_going = False
    if game_world != None:
        game_world.update()
        game_world.draw(screen)
    else:
        screen.fill((255, 255, 255))
    pygame.display.update()
    timer.tick(60)
    steps += 1
pygame.quit()
