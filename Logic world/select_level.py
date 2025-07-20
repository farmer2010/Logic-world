from image_factory import get_image
import pygame
pygame.init()

class SelectLevel():
    def __init__(self, menu, data):
        self.menu = menu
        self.data = data
        W = pygame.display.Info().current_w
        H = pygame.display.Info().current_h
        self.floor_img = pygame.Surface((W, H))
        for x in range(int(W / 40)):
            for y in range(int(H / 40)):
                self.floor_img.blit(get_image(1, 0), (x * 40, y * 40))

    def update(self, events):
        if pygame.mouse.get_pressed()[0]:
            mousepos = pygame.mouse.get_pos()
            pos = [mousepos[0] // 80, mousepos[1] // 80]
            self.menu[0] = "game"

    def draw(self, screen):
        screen.blit(self.floor_img, (0, 0))