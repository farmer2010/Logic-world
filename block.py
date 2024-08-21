from random import randint as rand
from image_factory import get_image
import pygame
pygame.init()

def get_data(type_):
    if type_ == "wire":
        return({"activated" : 0})
    elif type_ == "activator":
        return({"activated" : 0})
    else:
        return({})

class Block():
    def __init__(self, world, pos, sftype, glassed=0, data=None):
        self.world = world
        self.pos = pos
        self.type = sftype
        if data == None:
            self.data = get_data(self.type)
        else:
            self.data = data
        self.glassed = glassed
        self.image = pygame.Surface((40, 40))
        self.movelist = [
            [0, 1],
            [1, 0],
            [0, -1],
            [-1, 0]
        ]
        self.active = 0

    def change_image(self):
        if self.type == "air":
            self.image.fill((0, 0, 0))
            self.image.set_colorkey((0, 0, 0))
        elif self.type == "wire":
            see = [0, 0, 0, 0]
            for i in range(4):
                pos = [self.pos[0] + self.movelist[i][0], self.pos[1] + self.movelist[i][1]]
                if pos[0] >= 0 and pos[0] < self.world.w and pos[1] >= 0 and pos[1] < self.world.h:
                    b = self.world.field[pos[0]][pos[1]]
                    if b.type == "wire" or b.type == "activator":
                        see[i] = 1
            self.image = get_image(6 + see[0] * 2 + see[3] + 4 * self.data["activated"], see[2] * 2 + see[1])
        elif self.type == "activator":
            self.image = get_image(self.data["activated"], 2)
        elif self.type == "block":
            self.image = get_image(0, 1)
        if self.glassed:
            see = [0, 0, 0, 0]
            for i in range(4):
                pos = [self.pos[0] + self.movelist[i][0], self.pos[1] + self.movelist[i][1]]
                if pos[0] >= 0 and pos[0] < self.world.w and pos[1] >= 0 and pos[1] < self.world.h:
                    b = self.world.field[pos[0]][pos[1]]
                    if b.glassed:
                        see[i] = 1
            self.image.blit(get_image(2 + see[0] * 2 + see[3], see[2] * 2 + see[1]), (0, 0))

    def draw(self, screen, world_pos):
        screen.blit(self.image, (world_pos[0] + self.pos[0] * 40, world_pos[1] + self.pos[1] * 40))

    def action(self):#нажатие на блок
        if self.type == "activator":
            self.data["activated"] = not self.data["activated"]

    def update(self, data):#распространение энергии
        self.change_image()
        self.active = 1
        for i in range(4):
            pos = [self.pos[0] + self.movelist[i][0], self.pos[1] + self.movelist[i][1]]
            if pos[0] >= 0 and pos[0] < self.world.w and pos[1] >= 0 and pos[1] < self.world.h:
                b = self.world.field[pos[0]][pos[1]]
                if b.type == "wire" and b.active == 0:
                    b.data["activated"] = data["activated"]
                    b.update({"activated" : data["activated"]})
