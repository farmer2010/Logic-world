from blocks.block import Block
from blocks.image_factory import *

class NoPushable(Block):
    def __init__(self, world, pos, glassed=0, data=None):
        preset_data = {}
        Block.__init__(self, world, pos, "no pushable", glassed, data, preset_data)

    def get_pushable(self, rotate):
        return(0)

    def get_image(self):
        see = [0, 0, 0, 0]
        for i in range(4):
            pos = self.get_rotate_position(i)
            if self.border(pos):
                see[i] = self.world.field[pos[0]][pos[1]].type == "no pushable"
        return(get_image(see[2] * 2 + see[3], 12 + see[0] * 2 + see[1], size=self.world.block_scale))