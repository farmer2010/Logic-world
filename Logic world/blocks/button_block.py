from blocks.block import Block
from image_factory import *

class ButtonBlock(Block):
    def __init__(self, world, pos, glassed=0, data=None):
        preset_data = {"activated" : 0}
        Block.__init__(self, world, pos, "button", glassed, data, preset_data)
        self.has_output = 1
        self.has_action = 1

    def update(self, data={}, enr=1):
        self.active = 1
        if self.data["activated"]:
            for i in range(4):
                self.signal(i)
            self.data["activated"] -= 1

    def action(self):
        self.data["activated"] = 1

    def is_block_connect_with_wire(self, rotate):
        return(1)

    def is_block_connect_output(self, rotate):
        return(1)

    def get_output_activated_key(self, rotate):#-|-
        return("activated")

    def get_image(self):
        return(get_image(0, 3, size=self.world.block_scale))