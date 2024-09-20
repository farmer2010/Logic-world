from random import randint as rand
from image_factory import get_image
import pygame
pygame.init()

def get_data(type_):
    if type_ == "wire":
        return({"activated" : 0})
    elif type_ == "activator":
        return({"activated" : 0})
    elif type_ == "NOT":
        return({"activated" : 0, "rotate" : 0})
    elif type_ == "wire box":
        return({"activated1" : 0, "activated2" : 0})#горизонтальный, вертикальный
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
            [0, -1],
            [1, 0],
            [0, 1],
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
                pos = self.get_rotate_position(i)
                if self.border(pos):
                    see[i] = self.is_block_connect_with_wire(i)
            self.image = get_image(6 + see[2] * 2 + see[3] + 4 * self.data["activated"], see[0] * 2 + see[1])
        elif self.type == "activator":
            self.image = get_image(self.data["activated"], 2)
        elif self.type == "block":
            self.image = get_image(0, 1)
        elif self.type == "NOT":
            i = 0
            front_pos = self.get_rotate_position(self.data["rotate"])
            if self.border(front_pos):
                i = self.is_block_connect_with_wire(self.data["rotate"])
            self.image = get_image(10 + self.data["activated"] * 2 + i, 4 + self.data["rotate"])
        elif self.type == "wire box":
            self.image = get_image(0 + self.data["activated1"], 3 + self.data["activated2"])
        if self.glassed:
            see = [0, 0, 0, 0]
            for i in range(4):
                pos = self.get_rotate_position(i)
                if self.border(pos):
                    b = self.world.field[pos[0]][pos[1]]
                    if b.glassed:
                        see[i] = 1
            self.image.blit(get_image(2 + see[2] * 2 + see[3], see[0] * 2 + see[1]), (0, 0))

    def draw(self, screen, world_pos):
        screen.blit(self.image, (world_pos[0] + self.pos[0] * 40, world_pos[1] + self.pos[1] * 40))

    def action(self):#нажатие на блок
        if self.type == "activator":
            self.data["activated"] = not self.data["activated"]

    def update(self, data={}, enr=1):#распространение энергии
        if self.type == "NOT":
            front_pos = self.get_rotate_position(self.data["rotate"])
            behind_pos = self.get_rotate_position((self.data["rotate"] + 2) % 4)
            i = 0
            if self.border(behind_pos):
                behind_block = self.world.field[behind_pos[0]][behind_pos[1]]
                if behind_block.type == "wire" or behind_block.type == "activator" or behind_block.type == "NOT":
                    i = behind_block.data["activated"]
            self.data["activated"] = not i
            if not i == 1:
                self.active = 1
            if self.border(front_pos):
                front_block = self.world.field[front_pos[0]][front_pos[1]]
                if front_block.type == "wire" and front_block.active == 0 and self.data["activated"] and enr:
                    front_block.data["activated"] = self.data["activated"]
                    front_block.update({"rotate" : i})
        elif self.type == "wire box":
            if data["rotate"] == 1 or data["rotate"] == 3:#горизонтальный провод
                self.data["activated1"] = 1
            elif data["rotate"] == 0 or data["rotate"] == 2:#вертикальный провод
                self.data["activated2"] = 1
            pos = self.get_rotate_position(data["rotate"])
            if self.border(pos):
                b = self.world.field[pos[0]][pos[1]]
                if (b.type == "wire" or b.type == "wire box") and b.active == 0:
                    b.update({"rotate" : data["rotate"]})  
        else:#провод или активатор
            self.active = 1
            self.data["activated"] = 1
            for i in range(4):
                pos = self.get_rotate_position(i)
                if self.border(pos):
                    b = self.world.field[pos[0]][pos[1]]
                    if (b.type == "wire" or b.type == "wire box") and b.active == 0:
                        b.update({"rotate" : i})

    def get_rotate_position(self, rotate):
        return([self.pos[0] + self.movelist[rotate][0], self.pos[1] + self.movelist[rotate][1]])

    def border(self, pos):
        return(pos[0] >= 0 and pos[0] < self.world.w and pos[1] >= 0 and pos[1] < self.world.h)

    def is_block_connect_with_wire(self, rotate):
        pos = self.get_rotate_position(rotate)
        b = self.world.field[pos[0]][pos[1]]
        return(b.type == "wire" or b.type == "activator" or (b.type == "NOT" and (b.data["rotate"] == rotate or (b.data["rotate"] + 2) % 4 == rotate)) or b.type == "wire box")
