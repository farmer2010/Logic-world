import pygame
pygame.init()

class Block():
    def __init__(self, pos, sftype, glassed=0):
        self.pos = pos
        self.type = sftype
        self.glassed = glassed
        self.image = pygame.Surface((40, 40))
        self.change_image()

    def change_image(self):
        if self.type == "air":
            self.image = pygame.Surface((40, 40))
            self.image.set_colorkey((0, 0, 0))
        elif self.type == "wire":
            self.image = pygame.Surface((40, 40))
            self.image

    def draw(self, screen, world_pos):
        pass
