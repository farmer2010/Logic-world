import pygame
from block import Block
from air import Air
from image_factory import *

class PistonHead(Block):
    def __init__(self, world, pos, glassed=0, data=None):
        preset_data = {"rotate" : 0, "sticky" : 0}
        Block.__init__(self, world, pos, "piston head", glassed, data, preset_data)
        self.is_logic_gate = 1

    def update(self, data={}, enr=1):
        if enr == 0:
            behind_pos = self.get_rotate_position((self.data["rotate"] + 2) % 4)
            if self.border(behind_pos):
                if self.world.field[behind_pos[0]][behind_pos[1]].type != "piston":
                    self.world.field[self.pos[0]][self.pos[1]] = Air(self.world, self.pos)

    def get_pushable(self, rotate):
        return(0)

    def get_image(self):
        return(get_image(2 + self.data["sticky"], self.data["rotate"], size=self.world.block_scale))