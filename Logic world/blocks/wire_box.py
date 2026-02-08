from blocks.block import Block
from blocks.image_factory import *

class WireBox(Block):
    def __init__(self, world, pos, glassed=0, data=None):
        preset_data = {"activated1" : 0, "activated2" : 0}
        Block.__init__(self, world, pos, "wire box", glassed, data, preset_data)

    def update(self, data={}):
        if data["rotate"] == 1 or data["rotate"] == 3:#горизонтальный провод
            self.data["activated1"] = 1
        elif data["rotate"] == 0 or data["rotate"] == 2:#вертикальный провод
            self.data["activated2"] = 1
        pos = self.get_rotate_position(data["rotate"])
        #
        if self.border(pos):#распространение сигнала
            b = self.world.field[pos[0]][pos[1]]
            if (b.type == "wire" or b.type == "wire box" or b.type == "diode" or b.type == "output" or b.type == "armored wire") and b.active == 0:
                b.update({"rotate": data["rotate"]})

    def is_block_connect_with_wire(self, rotate):
        return(1)

    def is_block_connect_output(self, rotate):
        return(1)

    def is_block_connect_input(self, rotate):
        return(1)

    def get_activated_key(self, rotate):
        if rotate == 0 or rotate == 2:
            return("activated2")
        return("activated1")

    def get_image(self):
        return(get_image(7, self.data["activated1"] + self.data["activated2"] * 2 + 8, size=self.world.block_scale))