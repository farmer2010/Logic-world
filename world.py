import copy
from image_factory import get_image
import image_factory
from block import Block
import pygame
pygame.init

class World:
    def __init__(self, w=10, h=10, pos=[0, 0]):
        self.w = w
        self.h = h
        self.field = [[Block(self, (x, y), "air") for y in range(h)] for x in range(w)]
        self.pos = [pos[0] * 40, pos[1] * 40]
        self.is_set = True
        W = pygame.display.Info().current_w
        H = pygame.display.Info().current_h
        self.floor_img = pygame.Surface((W, H))
        for x in range(int(W / 40)):
            for y in range(int(H / 40)):
                if x >= pos[0] and x < pos[0] + self.w and y >= pos[1] and y < pos[1] + self.h:
                    self.floor_img.blit(get_image(1, 0), (x * 40, y * 40))
                else:
                    self.floor_img.blit(get_image(0, 0), (x * 40, y * 40))
        self.change_image()
        self.select_block = "air"
        self.mousetag = 0
        self.timer = 0
        self.select_rotate = 0
        self.r_tag = 0

    def update(self):
        keys = pygame.key.get_pressed()#проверка нажатий кнопок
        #смена блока "в руке"
        if keys[pygame.K_1]:
            self.select_block = "wire"
        elif keys[pygame.K_2]:
            self.select_block = "activator"
        elif keys[pygame.K_3]:
            self.select_block = "block"
        elif keys[pygame.K_4]:
            self.select_block = "NOT"
        elif keys[pygame.K_5]:
            self.select_block = "wire box"
        if keys[pygame.K_r]:#поворот блока
            if self.r_tag == 0:
                self.select_rotate += 1
                self.select_rotate %= 4
                self.r_tag = 1
        else:
            self.r_tag = 0
        if keys[pygame.K_q]:#пипетка
            mousepos = pygame.mouse.get_pos()
            mouse_world_pos = [mousepos[0] - self.pos[0], mousepos[1] - self.pos[1]]
            blockpos = [int(mouse_world_pos[0] / 40), int(mouse_world_pos[1] / 40)]
            if blockpos[0] >= 0 and blockpos[0] < self.w and blockpos[1] >= 0 and blockpos[1] < self.h:
                self.select_block = self.field[blockpos[0]][blockpos[1]].type
            else:
                self.select_block = "air"
        #установка и ломание
        if pygame.mouse.get_pressed()[0]:#установка
            mousepos = pygame.mouse.get_pos()
            mouse_world_pos = [mousepos[0] - self.pos[0], mousepos[1] - self.pos[1]]
            blockpos = [int(mouse_world_pos[0] / 40), int(mouse_world_pos[1] / 40)]
            if blockpos[0] >= 0 and blockpos[0] < self.w and blockpos[1] >= 0 and blockpos[1] < self.h:
                if self.field[blockpos[0]][blockpos[1]].type == "air":
                    if self.field[blockpos[0]][blockpos[1]].glassed == 0:
                        self.timer = 0
                        self.field[blockpos[0]][blockpos[1]] = Block(self, blockpos, self.select_block)
                        if self.select_block == "NOT":
                            self.field[blockpos[0]][blockpos[1]].data["rotate"] = self.select_rotate
                        self.change_image()
                        self.mousetag = 1
                elif self.mousetag == 0:#нажатие на блок
                    self.timer = 0
                    self.mousetag = 1
                    self.field[blockpos[0]][blockpos[1]].action()
                    self.change_image()
        else:
           self.mousetag = 0
        if pygame.mouse.get_pressed()[2]:#ломание
            mousepos = pygame.mouse.get_pos()
            mouse_world_pos = [mousepos[0] - self.pos[0], mousepos[1] - self.pos[1]]
            blockpos = [int(mouse_world_pos[0] / 40), int(mouse_world_pos[1] / 40)]
            if blockpos[0] >= 0 and blockpos[0] < self.w and blockpos[1] >= 0 and blockpos[1] < self.h:
                if self.field[blockpos[0]][blockpos[1]].glassed == 0:
                    self.timer = 0
                    self.field[blockpos[0]][blockpos[1]] = Block(self, blockpos, "air")
                    self.change_image()

        if self.timer == 0:
            for x in range(self.w):#стираем active
                for y in range(self.h):
                    self.field[x][y].active = 0
            for x in range(self.w):#стираем электричество
                for y in range(self.h):
                    if self.field[x][y].type == "wire":
                        self.field[x][y].data["activated"] = 0
                    elif self.field[x][y].type == "wire box":
                        self.field[x][y].data["activated1"] = 0
                        self.field[x][y].data["activated2"] = 0
            for x in range(self.w):#распространение электричества
                for y in range(self.h):
                    if self.field[x][y].type == "activator" or self.field[x][y].type == "NOT":
                        if self.field[x][y].data["activated"] == 1:
                            self.field[x][y].update()
            for x in range(self.w):#активация логических вентилей
                for y in range(self.h):
                    if self.field[x][y].type == "NOT":
                        self.field[x][y].update(self.field[x][y].data, enr=0)
            #gates = 1
            #while gates > 0:#активация логических вентилей
            #    gates = 0
            #    for x in range(self.w):
            #        for y in range(self.h):
            #            if self.field[x][y].type == "NOT" and self.field[x][y].active == 0:
            #                self.field[x][y].active = 1
            #                gates += 1
            #                self.field[x][y].update(self.field[x][y].data)
            self.change_image()

        self.timer = 0
        #self.timer += 1
        #if self.timer >= 60:
        #    self.timer = 0

    def draw(self, screen):
        font = pygame.font.SysFont(None, 25)
        screen.fill((90, 90, 90))
        screen.blit(self.floor_img, [0, 0])
        for x in range(self.w):
            for y in range(self.h):
                self.field[x][y].draw(screen, self.pos)
        mousepos = pygame.mouse.get_pos()
        mouse_world_pos = [mousepos[0] - self.pos[0], mousepos[1] - self.pos[1]]
        blockpos = [int(mouse_world_pos[0] / 40), int(mouse_world_pos[1] / 40)]
        if blockpos[0] >= 0 and blockpos[0] < self.w and blockpos[1] >= 0 and blockpos[1] < self.h:
            if self.field[blockpos[0]][blockpos[1]].type == "air":
                if self.select_block != "air":
                    select_image = image_factory.get_block_image(self.select_block, [0, 0, 0, 0], {"activated" : 0, "rotate" : self.select_rotate, "activated1" : 0, "activated2" : 0})
                    select_image.convert_alpha()
                    select_image.set_alpha(90)
                else:
                    select_image = image_factory.get_block_image("air", [], {})
                screen.blit(select_image, (blockpos[0] * 40 + self.pos[0], blockpos[1] * 40 + self.pos[1]))

    def change_image(self):
        for x in range(self.w):
            for y in range(self.h):
                self.field[x][y].change_image()
