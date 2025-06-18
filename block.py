from image_factory import *
import pygame
pygame.init()

class Block():
    def __init__(self, world, pos, sftype, glassed=0, data=None, preset_data={}):
        self.world = world
        self.pos = pos
        self.world.field[self.pos[0]][self.pos[1]] = self
        self.type = sftype
        self.glassed = glassed
        if data == None:
            self.data = preset_data
        else:
            self.data = data
        self.image = pygame.Surface((40, 40))
        self.movelist = [
            [0, -1],
            [1, 0],
            [0, 1],
            [-1, 0]
        ]
        self.diag_movelist = [
            [-1, -1],
            [1, -1],
            [1, 1],
            [-1, 1]
        ]
        self.active = 0
        self.is_logic_gate = 0
        self.has_output = 0

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
        elif self.type == "memory":#ячейка памяти
            self.image = get_memory_image(self.data)
        elif self.type == "sensor":#сенсор
            self.image = get_sensor_image(self.data)
        elif self.type == "energy block":#блок сигнала
            self.image = get_image(1, 3)
        elif self.type == "button":
            self.image = get_image(0, 3)
        if self.glassed:
            see = [0, 0, 0, 0]
            see2 = [0, 0, 0, 0]
            for i in range(4):
                pos = self.get_rotate_position(i)
                if self.border(pos):
                    b = self.world.field[pos[0]][pos[1]]
                    if b.glassed:
                        see[i] = 1
            for i in range(4):
                pos = [self.pos[0] + self.diag_movelist[i][0], self.pos[1] + self.diag_movelist[i][1]]
                if self.border(pos):
                    b = self.world.field[pos[0]][pos[1]]
                    if b.glassed:
                        see2[i] = 1
            img = get_image(6 + see[2] * 2 + see[3], 12 + see[0] * 2 + see[1], size=10)
            if see[0] and see[1] and not see2[1]:
                img.set_at((9, 0), (170, 181, 193))
            if see[1] and see[2] and not see2[2]:
                img.set_at((9, 9), (170, 181, 193))
            if see[2] and see[3] and not see2[3]:
               img.set_at((0, 9), (170, 181, 193))
            if see[3] and see[0] and not see2[0]:
                img.set_at((0, 0), (170, 181, 193))
            self.image.blit(pygame.transform.scale(img, (40, 40)), (0, 0))

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

    def is_block_connect_with_wire(self, rotate):#используется направление, ПРОТИВОПОЛОЖНОЕ направлению к блоку, с которым проверяем соединение(если блок сверху(0), в функции должно быть "вниз"(2))
         return(0)

    def is_block_connect_output(self, rotate):#-|-
        return(0)

    def is_block_connect_input(self, rotate):#-|-
        return(0)

    def get_activated_key(self, rotate):#-|-
        return(None)

    def connect_with_armored_wire(self):
        pass

from wire import Wire
from activator import Activator
from NOT import NOT
from logic_gate import LogicGate
from armored_wire import ArmoredWire
from diode import Diode
from output import Output
from wire_box import WireBox
from memory import Memory
from sensor import Sensor
from energy_block import EnergyBlock
from button_block import ButtonBlock

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
    elif type == "memory":
        return(Memory(world, pos, glassed, data))
    elif type == "sensor":
        return(Sensor(world, pos, glassed, data))
    elif type == "energy block":
        return(EnergyBlock(world, pos, glassed, data))
    elif type == "button":
        return (ButtonBlock(world, pos, glassed, data))
    return(Block(world, pos, type, glassed, data))