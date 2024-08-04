from block import Block
import pygame
pygame.init

class World:
    def __init__(self, w=10, h=10):
        self.w = w
        self.h = h
        self.field = [[Block((w, h), "air") for y in range(h)] for x in range(w)]
        self.pos = [0, 0]
        

    def update(self):
        pass

    def draw(self, screen):
        screen.fill((90, 90, 90))
        pygame.draw.rect(screen, (50, 50, 50), (self.pos[0], self.pos[1], self.w * 40, self.h * 40))
