from block import Block
from image_factory import *

class Output(Block):
    def __init__(self, world, pos, glassed=0, data=None):
        preset_data = {"activated" : 0, "rotate" : 0}
        Block.__init__(self, world, pos, "output", glassed, data, preset_data)

    def update(self, data={}):
        if data["rotate"] == self.data["rotate"]:
            self.active = 1
            self.data["activated"] = 1

    def is_block_connect_with_wire(self, rotate):
        return(self.data["rotate"] == rotate)

    def is_block_connect_input(self, rotate):
        return (self.data["rotate"] == rotate)

    def get_activated_key(self, rotate):#-|-
        return("activated")

    def get_image(self):
        return(get_image(self.data["activated"], 4 + self.data["rotate"], size=self.world.block_scale))