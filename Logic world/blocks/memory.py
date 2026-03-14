from blocks.block import Block
from image_factory import *

class Memory(Block):
    def __init__(self, world, pos, glassed=0, data=None):
        preset_data = {"activated1" : 0, "activated2" : 0, "activated" : 0, "rotate" : 0, "inverted" : 0}
        Block.__init__(self, world, pos, "memory", glassed, data, preset_data)
        self.is_logic_gate = 1
        self.has_output = 1

    def update(self, data={}, enr=1):
        if not enr:
            s = self.data["activated"]
            #активация
            if not self.data["inverted"]:
                if (self.data["activated1"] and self.data["activated2"] != self.data["activated"]):
                    self.logic_gate_active = 1
                    self.data["activated"] = self.data["activated2"]
            else:
                if (self.data["activated2"] and self.data["activated1"] != self.data["activated"]):
                    self.logic_gate_active = 1
                    self.data["activated"] = self.data["activated1"]
            #
            self.active = self.data["activated"]
            if self.data["activated"] != s:
                self.logic_gate_active = 1
        #распространение сигнала
        if enr:
            self.signal(self.data["rotate"])

    def is_block_connect_with_wire(self, rotate):
        return(self.data["rotate"] != rotate)

    def is_block_connect_output(self, rotate):
        return((self.data["rotate"] + 2) % 4 == rotate)

    def is_block_connect_input(self, rotate):
        return((self.data["rotate"] + 1) % 4 == (rotate + 2) % 4 or (self.data["rotate"] - 1) % 4 == (rotate + 2) % 4)

    def get_output_activated_key(self, rotate):
        return("activated")

    def get_input_activated_key(self, rotate):
        if rotate == (self.data["rotate"] + 1) % 4:
            return("activated1")
        elif rotate == (self.data["rotate"] - 1) % 4:
            return ("activated2")

    def clear_inputs(self):
        self.data["activated1"] = 0
        self.data["activated2"] = 0

    def get_image(self):
        if not self.data["inverted"]:
            p = self.data["activated1"] + self.data["activated2"] * 2 + self.data["activated"] * 4
        else:
            p = self.data["activated2"] + self.data["activated1"] * 2 + self.data["activated"] * 4
        return (get_image(8 + p - 1 * (p > 2) - 1 * (p > 4) + self.data["inverted"] * 6, self.data["rotate"] + 8, size=self.world.block_scale))