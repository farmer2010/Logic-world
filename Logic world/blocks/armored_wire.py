from blocks.block import Block
from image_factory import *

class ArmoredWire(Block):
    def __init__(self, world, pos, glassed=0, data=None):
        preset_data = {"activated": 0, "connections" : [0, 0, 0, 0]}
        Block.__init__(self, world, pos, "armored wire", glassed, data, preset_data)

    def update(self, data={}):
        if self.data["connections"][(data["rotate"] + 2) % 4]:
            self.active = 1
            self.data["activated"] = 1
            for i in range(4):
                if self.data["connections"][i]:
                    self.signal(i)

    def is_block_connect_with_wire(self, rotate):
        return(self.data["connections"][(rotate + 2) % 4])

    def is_block_connect_with_armored_wire(self, rotate):
        return(sum(self.data["connections"]) - self.data["connections"][(rotate + 2) % 4] <= 1)

    def is_block_connect_output(self, rotate):
        return(sum(self.data["connections"]) - self.data["connections"][(rotate + 2) % 4] <= 1)

    def is_block_connect_input(self, rotate):
        return(sum(self.data["connections"]) - self.data["connections"][(rotate + 2) % 4] <= 1)

    def get_output_activated_key(self, rotate):#-|-
        return("activated")

    def get_input_activated_key(self, rotate):
        return("activated")

    def get_image(self):
        return(get_image(4 + self.data["connections"][2] * 2 + self.data["connections"][3] + 4 * self.data["activated"], 4 + self.data["connections"][0] * 2 + self.data["connections"][1], size=self.world.block_scale))

    def connect_with_armored_wire(self):
        see = [0, 0, 0, 0]
        for i in range(4):
            pos = self.get_rotate_position(i)
            if self.border(pos):
                see[i] = self.world.field[pos[0]][pos[1]].is_block_connect_with_armored_wire(i)
        if sum(see) <= 2:
            self.data["connections"] = see.copy()
            for i in range(4):
                pos = self.get_rotate_position(i)
                if self.border(pos):
                    if self.world.field[pos[0]][pos[1]].type == "armored wire" and self.world.field[pos[0]][pos[1]].is_block_connect_with_armored_wire(i) and self.is_block_connect_with_armored_wire((i + 2) % 4):
                        self.world.field[pos[0]][pos[1]].data["connections"][(i + 2) % 4] = 1

    def connect_armored_wires(self):
        for i in range(4):
            pos = self.get_rotate_position(i)
            if self.border(pos):
                if self.world.field[pos[0]][pos[1]].type == "armored wire" and self.data["connections"][i]:
                    self.world.field[pos[0]][pos[1]].data["connections"][(i + 2) % 4] = 1
                elif self.world.field[pos[0]][pos[1]].type == "armored wire" and self.world.field[pos[0]][pos[1]].data["connections"] and self.data["connections"][i] == 0:
                    self.world.field[pos[0]][pos[1]].data["connections"][(i + 2) % 4] = 0