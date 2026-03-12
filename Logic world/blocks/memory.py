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
            la = 0
            ra = 0
            s = self.data["activated"]
            #левый вход
            left_pos = self.get_rotate_position((self.data["rotate"] - 1) % 4)
            if self.border(left_pos):
                left_block = self.world.field[left_pos[0]][left_pos[1]]
                la = left_block.logic_gate_active
            #правый вход
            right_pos = self.get_rotate_position((self.data["rotate"] + 1) % 4)
            if self.border(right_pos):
                right_block = self.world.field[right_pos[0]][right_pos[1]]
                ra = right_block.logic_gate_active
            #активация
            if la == 0 and ra == 0:
                if (self.data["activated1"] and self.data["activated2"] != self.data["activated"]):
                    self.logic_gate_active = 1
                    self.data["activated"] = self.data["activated2"]
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

    def clear_inputs(self):
        self.data["activated1"] = 0
        self.data["activated2"] = 0

    def get_image(self):
        p = self.data["activated1"] + self.data["activated2"] * 2 + self.data["activated"] * 4
        return (get_image(8 + p - 1 * (p > 2) - 1 * (p > 4), self.data["rotate"] + 8, size=self.world.block_scale))