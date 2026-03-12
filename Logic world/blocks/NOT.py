from blocks.block import Block
from image_factory import *

class NOT(Block):
    def __init__(self, world, pos, glassed=0, data=None):
        preset_data = {"activated" : 0, "rotate" : 0}
        Block.__init__(self, world, pos, "NOT", glassed, data, preset_data)
        self.is_logic_gate = 1
        self.has_output = 1

    def update(self, data={}, enr=1):
        if not enr:
            behind_pos = self.get_rotate_position((self.data["rotate"] + 2) % 4)
            inp = 0
            ba = 1
            #вход
            s = self.data["activated"]
            if self.border(behind_pos):
                behind_block = self.world.field[behind_pos[0]][behind_pos[1]]
                if behind_block.is_block_connect_output((self.data["rotate"] + 2) % 4):
                    inp = behind_block.data[behind_block.get_output_activated_key((self.data["rotate"] + 2) % 4)]
                ba = behind_block.logic_gate_active
            #активация
            if ba == 0:
                self.data["activated"] = not inp
            self.active = not inp
            if self.data["activated"] != s:
                self.logic_gate_active = 1
        if enr:#распространение сигнала
            self.signal(self.data["rotate"])


    def is_block_connect_with_wire(self, rotate):
        return(self.data["rotate"] == rotate or (self.data["rotate"] + 2) % 4 == rotate)

    def is_block_connect_output(self, rotate):
        return((self.data["rotate"] + 2) % 4 == rotate)

    def is_block_connect_input(self, rotate):
        return(self.data["rotate"] == rotate)

    def get_output_activated_key(self, rotate):#-|-
        return("activated")

    def get_image(self):
        i = 0
        front_pos = self.get_rotate_position(self.data["rotate"])
        if self.border(front_pos):
            i = self.world.field[front_pos[0]][front_pos[1]].is_block_connect_with_wire(self.data["rotate"])
            if self.world.field[front_pos[0]][front_pos[1]].type == "armored wire":
                i = self.world.field[front_pos[0]][front_pos[1]].data["connections"][(self.data["rotate"] + 2) % 4]
        return(get_image(12 + self.data["activated"] * 2 + i, 4 + self.data["rotate"], size=self.world.block_scale))