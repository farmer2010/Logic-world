#настройка
import pygame
from ui import UI

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
#game_world = World(int(W / 40), int(H / 40))
#
#data = [11, 11, 18, 8, "1"]

class Main():
    def __init__(self):
       self.menu = UI(self, [str(int(W / 40)), str(int(H / 40)), "0", "0", "1"])
game_world = Main()

while keep_going:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:#проверка выхода
            keep_going = False
    game_world.menu.draw(screen)
    game_world.menu.update(events)
    pygame.display.update()
    timer.tick(60)
    steps += 1
pygame.quit()