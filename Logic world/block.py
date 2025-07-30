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
        self.image = pygame.Surface((self.world.block_scale, self.world.block_scale))
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
        self.logic_gate_active = 0
        self.is_logic_gate = 0
        self.has_output = 0
        self.has_action = 0

    def __str__(self):
        s = f"{self.type} at {str(self.pos)}\n"
        param = self.data.keys()
        for p in param:
            s += f"{p}: {str(self.data[p])}\n"
        s = s[:len(s) - 1]
        return(s)

    def change_image(self):#сменить картинку
        self.image = self.get_image()
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
            img = get_image(4 + see[2] * 2 + see[3], see[0] * 2 + see[1], size=10)
            if see[0] and see[1] and not see2[1]:
                img.set_at((9, 0), (170, 181, 193))
            if see[1] and see[2] and not see2[2]:
                img.set_at((9, 9), (170, 181, 193))
            if see[2] and see[3] and not see2[3]:
               img.set_at((0, 9), (170, 181, 193))
            if see[3] and see[0] and not see2[0]:
                img.set_at((0, 0), (170, 181, 193))
            self.image.blit(pygame.transform.scale(img, (self.world.block_scale, self.world.block_scale)), (0, 0))

    def get_image(self):
        image = pygame.Surface((self.world.block_scale, self.world.block_scale))
        return(image)

    def draw(self, screen, world_pos):
        screen.blit(self.image, (world_pos[0] + self.pos[0] * self.world.block_scale, world_pos[1] + self.pos[1] * self.world.block_scale))

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

    def is_block_connect_with_armored_wire(self, rotate):
        return(self.is_block_connect_with_wire(rotate))

    def is_block_connect_output(self, rotate):#-|-
        return(0)

    def is_block_connect_input(self, rotate):#-|-
        return(0)

    def get_activated_key(self, rotate):#-|-
        return(None)

    def get_pushable(self, rotate):#-|-
        return(1)

    def connect_with_armored_wire(self):
        for i in range(4):
            pos = self.get_rotate_position(i)
            if self.border(pos):
                if self.world.field[pos[0]][pos[1]].type == "armored wire" and self.world.field[pos[0]][pos[1]].is_block_connect_with_armored_wire(i) and self.is_block_connect_with_wire((i + 2) % 4):
                    self.world.field[pos[0]][pos[1]].data["connections"][(i + 2) % 4] = 1

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
from piston import Piston
from brick import Brick
from piston_head import PistonHead

def get_block(world, pos, type, glassed=0, data=None):
    if type == "air":
        return (Wire(world, pos, glassed, data))
    elif type == "block":
        return(Brick(world, pos, glassed, data))
    elif type == "wire":
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
    elif type == "piston":
        return(Piston(world, pos, glassed, data))
    elif type == "piston head":
        return (PistonHead(world, pos, glassed, data))
    return(Block(world, pos, type, glassed, data))

def get_block_params(type):
    if type == "wire":
        return({"activated" : 0})
    elif type == "activator":
        return({"activated" : 0})
    elif type == "NOT":
        return({"activated" : 0, "rotate" : 0})
    elif type == "XOR" or type == "AND":
        return({"activated1" : 0, "activated2" : 0, "activated" : 0, "rotate" : 0})
    elif type == "armored wire":
        return({"activated": 0, "connections" : [0, 0, 0, 0]})
    elif type == "diode":
        return({"activated1": 0, "activated2": 0, "rotate" : 0})
    elif type == "output":
        return({"activated" : 0, "rotate" : 0})
    elif type == "wire box":
        return({"activated1" : 0, "activated2" : 0})
    elif type == "memory":
        return({"activated1" : 0, "activated2" : 0, "activated" : 0, "rotate" : 0, "inverted" : 0})
    elif type == "sensor":
        return({"activated" : 0, "rotate" : 0})
    elif type == "energy block":
        return({"activated" : 1})
    elif type == "button":
        return ({"activated" : 0})
    elif type == "piston":
        return({"activated" : 0, "rotate" : 0})
    elif type == "piston head":
        return ({"rotate": 0, "sticky" : 0})
    else:
        return({})