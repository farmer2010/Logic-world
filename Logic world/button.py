import pygame
pygame.init()

class Button(pygame.sprite.Sprite):
    def __init__(self, world, image, pos, onclick, param):
        pygame.sprite.Sprite.__init__(self)
        self.pos = pos
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.onclick = onclick
        self.param = param

    def update(self):
        if pygame.MOUSEBUTTONDOWN and self.collide_point(pygame.mouse.get_pos()):
            onclick(self.param)

    def collide_point(self, pos):
        return((pos[0] >= self.pos[0] and pos[1] >= self.pos[1]) and (pos[0] <= self.pos[0] + self.image.get_width() and pos[1] <= self.pos[1] + self.image.get_height()))