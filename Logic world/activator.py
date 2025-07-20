import pygame
from block import Block

class Activator(Block):
    def __init__(self, world, pos, glassed=0, data=None):
        preset_data = {"activated" : 0}
        Block.__init__(self, world, pos, "activator", glassed, data, preset_data)
        self.has_output = 1

    def update(self, data={}, enr=1):
        self.active = 1
        if self.data["activated"]:
            for i in range(4):
                pos = self.get_rotate_position(i)
                if self.border(pos):
                    b = self.world.field[pos[0]][pos[1]]
                    if (b.type == "wire" or b.type == "wire box" or b.type == "diode" or b.type == "output" or (b.type == "armored wire" and b.data["connections"][(i + 2) % 4])) and b.active == 0:
                        b.update({"rotate": i})

    def action(self):
        self.data["activated"] = not self.data["activated"]

    def is_block_connect_with_wire(self, rotate):
        return(1)

    def is_block_connect_output(self, rotate):
        return(1)

    def get_activated_key(self, rotate):#-|-
        return("activated")

    def connect_with_armored_wire(self):
        for i in range(4):
            pos = self.get_rotate_position(i)
            if self.border(pos):
                if self.world.field[pos[0]][pos[1]].type == "armored wire" and self.world.field[pos[0]][pos[1]].is_block_connect_with_wire(i):
                    self.world.field[pos[0]][pos[1]].data["connections"][(i + 2) % 4] = 1