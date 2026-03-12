from blocks.block import Block
from image_factory import *

class Diode(Block):
    def __init__(self, world, pos, glassed=0, data=None):
        preset_data = {"activated1": 0, "activated2": 0, "rotate" : 0}
        Block.__init__(self, world, pos, "diode", glassed, data, preset_data)

    def update(self, data={}, enr=1):
        if data["rotate"] == self.data["rotate"]:
            self.active = 1
            self.data["activated1"] = 1
            self.data["activated2"] = 1
            self.signal(self.data["rotate"])

    def is_block_connect_with_wire(self, rotate):
        return(self.data["rotate"] == rotate or (self.data["rotate"] + 2) % 4 == rotate)

    def is_block_connect_output(self, rotate):
        return((self.data["rotate"] + 2) % 4 == rotate)

    def is_block_connect_input(self, rotate):
        return(self.data["rotate"] == rotate or self.data["rotate"] == (rotate + 2) % 4)

    def get_output_activated_key(self, rotate):
        return("activated2")

    def get_input_activated_key(self, rotate):
        if self.data["rotate"] == rotate:
            return("activated1")
        elif self.data["rotate"] == (rotate + 2) % 4:
            return("activated2")
        return(None)

    def clear_inputs(self):
        self.data["activated1"] = 0
        self.data["activated2"] = 0

    def get_image(self):
        return(get_image(4 + self.data["activated1"] + self.data["activated2"], 8 + self.data["rotate"], size=self.world.block_scale))