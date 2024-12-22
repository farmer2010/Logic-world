from image_factory import get_image
from button import Button
import image_factory
import pygame
pygame.init()

def render_text(text, pos, screen, color=(0, 0, 0), size=24, centerx=False, centery=False):#отрисовка текста на экране
    font = pygame.font.SysFont(None, size)
    text_img = font.render(text, True, color)
    text_rect = text_img.get_rect()
    if centerx:
        text_rect.centerx = pos[0]
    else:
        text_rect.x = pos[0]
    if centery:
        text_rect.centery = pos[1]
    else:
        text_rect.y = pos[1]
    screen.blit(text_img, text_rect)

class UI:
    def __init__(self, menu, data):
        self.menu = menu
        W = pygame.display.Info().current_w
        H = pygame.display.Info().current_h
        self.floor_img = pygame.Surface((W, H))
        self.floor_img.fill((30, 30, 30))
        #for x in range(int(W / 40)):
        #    for y in range(int(H / 40)):
        #            self.floor_img.blit(get_image(1, 0), (x * 40, y * 40))
        self.index = 0
        #self.data = [str(int(W / 40)), str(int(H / 40)), "0", "0", "1"]
        self.data = ["11", "11", "18", "8", "1"]
        self.ret_data = data

    def update(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if self.index > 0:
                        self.index -= 1
                if event.key == pygame.K_DOWN:
                    if self.index < 4:
                        self.index += 1
                if event.key == pygame.K_BACKSPACE:
                    self.data[self.index] = self.data[self.index][:len(self.data[self.index]) - 1]
                if event.key == pygame.K_RETURN:
                    for i in range(4):
                        self.ret_data[i] = int(self.data[i])
                    self.ret_data[4] = "level" + self.data[4]
                    self.menu[0] = "game"
                if event.key == pygame.K_0:
                    self.data[self.index] = self.data[self.index] + "0"
                if event.key == pygame.K_1:
                    self.data[self.index] = self.data[self.index] + "1"
                if event.key == pygame.K_2:
                    self.data[self.index] = self.data[self.index] + "2"
                if event.key == pygame.K_3:
                    self.data[self.index] = self.data[self.index] + "3"
                if event.key == pygame.K_4:
                    self.data[self.index] = self.data[self.index] + "4"
                if event.key == pygame.K_5:
                    self.data[self.index] = self.data[self.index] + "5"
                if event.key == pygame.K_6:
                    self.data[self.index] = self.data[self.index] + "6"
                if event.key == pygame.K_7:
                    self.data[self.index] = self.data[self.index] + "7"
                if event.key == pygame.K_8:
                    self.data[self.index] = self.data[self.index] + "8"
                if event.key == pygame.K_9:
                    self.data[self.index] = self.data[self.index] + "9"
                if event.key == pygame.K_PERIOD:
                    if self.index == 4:
                        self.data[self.index] = self.data[self.index] + "."

    def draw(self, screen):
        screen.blit(self.floor_img, (0, 0))
        pygame.draw.rect(screen, (200, 200, 0), (0, 100 * self.index, 20, 100))
        render_text("W: " + self.data[0], (20, 0), screen, size=100)
        render_text("H: " + self.data[1], (20, 100), screen, size=100)
        render_text("X: " + self.data[2], (20, 200), screen, size=100)
        render_text("Y: " + self.data[3], (20, 300), screen, size=100)
        render_text("NAME: " + self.data[4], (20, 400), screen, size=100)

