from blocks.block import Block
from image_factory import *

class Wire(Block):
    def __init__(self, world, pos, glassed=0, data=None):
        preset_data = {"activated" : 0}
        Block.__init__(self, world, pos, "wire", glassed, data, preset_data)

    def update(self, data={}):
        self.active = 1
        self.data["activated"] = 1
        for i in range(4):
            pos = self.get_rotate_position(i)
            if self.border(pos):
                b = self.world.field[pos[0]][pos[1]]
                if (b.type == "wire" or b.type == "wire box" or b.type == "diode" or b.type == "output" or (b.type == "armored wire" and b.data["connections"][(i + 2) % 4])) and b.active == 0:
                    b.update({"rotate": i})

    def is_block_connect_with_wire(self, rotate):
        return(1)

    def is_block_connect_output(self, rotate):
        return(1)

    def is_block_connect_input(self, rotate):
        return(1)

    def get_activated_key(self, rotate):#-|-
        return("activated")

    def get_image(self):
        see = [0, 0, 0, 0]
        for i in range(4):
            pos = self.get_rotate_position(i)
            if self.border(pos):
                see[i] = self.world.field[pos[0]][pos[1]].is_block_connect_with_wire(i)
                if self.world.field[pos[0]][pos[1]].type == "armored wire":
                    see[i] = self.world.field[pos[0]][pos[1]].data["connections"][(i + 2) % 4]
        return(get_image(8 + see[2] * 2 + see[3] + 4 * self.data["activated"], see[0] * 2 + see[1], size=self.world.block_scale))