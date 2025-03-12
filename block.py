from image_factory import *
import pygame
pygame.init()

class Block():
    def __init__(self, world, pos, sftype, glassed=0, data=None):
        self.world = world
        self.pos = pos
        self.world.field[self.pos[0]][self.pos[1]] = self
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
        #---------------------------------------------------------------------------------------------------------------
        if self.type == "armored wire":
            see = [0, 0, 0, 0]
            for i in range(4):
                pos = self.get_rotate_position(i)
                if self.border(pos):
                    see[i] = self.world.field[pos[0]][pos[1]].is_block_connect_with_wire(i)
        if self.type == "wire" or self.type == "armored wire" or self.type == "activator" or self.type == "NOT" or self.type == "AND" or self.type == "XOR" or self.type == "wire box" or self.type == "diode" or self.type == "output":
            for i in range(4):
                pos = self.get_rotate_position(i)
                if self.border(pos):
                    if self.world.field[pos[0]][pos[1]].type == "armored wire" and self.world.field[pos[0]][pos[1]].is_block_connect_with_wire(i) and self.is_block_connect_with_wire((i + 2) % 4):
                        self.world.field[pos[0]][pos[1]].data["connections"][(i + 2) % 4] = 1
        if self.type == "armored wire":
            if sum(see) <= 2:
                self.data["connections"] = see.copy()

    def change_image(self):#сменить картинку
        if self.type == "air":#воздух
            self.image.fill((0, 0, 0))
            self.image.set_colorkey((0, 0, 0))
        elif self.type == "wire":#провод
            see = [0, 0, 0, 0]
            for i in range(4):
                pos = self.get_rotate_position(i)
                if self.border(pos):
                    see[i] = self.world.field[pos[0]][pos[1]].is_block_connect_with_wire(i)
            self.image = get_wire_image(self.data, see)
        elif self.type == "activator":#активатор
            self.image = get_activator_image(self.data)
        elif self.type == "block":#кирпич
            self.image = get_image(0, 1)
        elif self.type == "NOT":#логический вентиль NOT
            i = 0
            front_pos = self.get_rotate_position(self.data["rotate"])
            if self.border(front_pos):
                i = self.world.field[front_pos[0]][front_pos[1]].is_block_connect_with_wire(self.data["rotate"])
            self.image = get_NOT_image(self.data, [i, 0, 0, 0])
        elif self.type == "wire box":#распределительная коробка
            self.image = get_wire_box_image(self.data)
        elif self.type == "AND":#логический вентиль AND
            self.image = get_AND_image(self.data)
        elif self.type == "XOR":#логический вентиль XOR
            self.image = get_XOR_image(self.data)
        elif self.type == "diode":#диод
            self.image = get_diode_image(self.data)
        elif self.type == "output":#лампа выхода
            self.image = get_output_image(self.data)
        elif self.type == "armored wire":#защищенный провод
            self.image = get_armored_wire_image(self.data, self.data["connections"])
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
        pass

    def update(self, data={}, enr=1):#распространение энергии
        pass

    def get_rotate_position(self, rotate):
        return([self.pos[0] + self.movelist[rotate][0], self.pos[1] + self.movelist[rotate][1]])

    def border(self, pos):
        return(pos[0] >= 0 and pos[0] < self.world.w and pos[1] >= 0 and pos[1] < self.world.h)

    def is_block_connect_with_wire(self, rotate):
         return(0)

from wire import Wire
from activator import Activator
from NOT import NOT
from logic_gate import LogicGate
from armored_wire import ArmoredWire
from diode import Diode
from output import Output
from wire_box import WireBox
def get_block(world, pos, type, glassed=0, data=None):
    if type == "wire":
        return(Wire(world, pos, glassed, data))
    elif type == "activator":
        return(Activator(world, pos, glassed, data))
    elif type == "NOT":
        return(NOT(world, pos, glassed, data))
    elif type == "XOR" or type == "AND":
        return(LogicGate(world, pos, type, glassed, data))
    elif type == "armored wire":
        return(ArmoredWire(world, pos, glassed, data))
    elif type == "diode":
        return(Diode(world, pos, glassed, data))
    elif type == "output":
        return(Output(world, pos, glassed, data))
    elif type == "wire box":
        return(WireBox(world, pos, glassed, data))

def get_data(type_):
    if type_ == "wire" or type_ == "activator":
        return({"activated" : 0})
    elif type_ == "NOT" or type_ == "output":
        return({"activated" : 0, "rotate" : 0})
    elif type_ == "wire box":
        return({"activated1" : 0, "activated2" : 0})#горизонтальный, вертикальный
    elif type_ == "AND" or type_ == "XOR" or type_ == "memory":
        return({"activated1" : 0, "activated2" : 0, "activated" : 0, "rotate" : 0})#левый относительно выхода, правый относительно выхода
    elif type_ == "diode":
        return ({"activated1": 0, "activated2": 0, "rotate" : 0})#задний, передний
    elif type_ == "armored wire":
        return ({"activated": 0, "connections" : [0, 0, 0, 0]})
    else:
        return({})
