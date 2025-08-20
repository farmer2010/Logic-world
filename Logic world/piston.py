import pygame
from block import *
from image_factory import *
from piston_head import PistonHead
from air import Air

class Piston(Block):
    def __init__(self, world, pos, type, glassed=0, data=None):
        preset_data = {"activated" : 0, "rotate" : 0, "power" : 12}
        Block.__init__(self, world, pos, type, glassed, data, preset_data)
        self.is_logic_gate = 1

    def update(self, data={}, enr=1):
        if enr == 0:
            inp = 0
            for i in range(3):
                pos = self.get_rotate_position((self.data["rotate"] + 1 + i) % 4)
                if self.border(pos):
                    behind_block = self.world.field[pos[0]][pos[1]]
                    if behind_block.is_block_connect_output((self.data["rotate"] + 2) % 4) and behind_block.logic_gate_active == 0:
                        inp = inp or behind_block.data[behind_block.get_activated_key((self.data["rotate"] + 2) % 4)]
            if inp:
                if self.data["activated"] == 0:
                    push = 0
                    count = self.data["power"]
                    a = 0
                    for i in range(self.data["power"] + 1):
                        pos = self.get_rotate_position(self.data["rotate"], dist=i + 1)
                        if self.border(pos):
                            if self.world.field[pos[0]][pos[1]].get_pushable(self.data["rotate"]) == 0:
                                break
                            if self.world.field[pos[0]][pos[1]].type == "air":
                                a = 1
                                if i > 0:
                                    print(1)
                                    push = 1
                                    count = i
                                break
                        else:
                            break
                    if push:
                        for i in range(count, 0, -1):
                            pos = self.get_rotate_position(self.data["rotate"], dist=i)
                            pos2 = self.get_rotate_position(self.data["rotate"], dist=i + 1)
                            self.world.field[pos2[0]][pos2[1]] = self.world.field[pos[0]][pos[1]]
                            self.world.field[pos2[0]][pos2[1]].pos = pos2
                            self.world.field[pos[0]][pos[1]] = Air(self.world, pos)
                    if a:
                        self.data["activated"] = 1
                        front_pos = self.get_rotate_position(self.data["rotate"])
                        if self.border(front_pos):
                            self.world.field[front_pos[0]][front_pos[1]] = PistonHead(self.world, front_pos, data={"rotate" : self.data["rotate"], "sticky" : "sticky" in self.type})
            else:
                if self.data["activated"] == 1:
                    self.data["activated"] = 0
                    front_pos = self.get_rotate_position(self.data["rotate"])
                    if self.border(front_pos):
                        if self.type == "piston":
                            self.world.field[front_pos[0]][front_pos[1]] = Air(self.world, front_pos)
                        else:
                            front_pos2 = self.get_rotate_position(self.data["rotate"], dist=2)
                            if self.border(front_pos2) and self.world.field[front_pos2[0]][front_pos2[1]].get_pushable((self.data["rotate"] + 2) % 4):
                                self.world.field[front_pos[0]][front_pos[1]] = self.world.field[front_pos2[0]][front_pos2[1]]
                                self.world.field[front_pos[0]][front_pos[1]].pos = front_pos
                                self.world.field[front_pos2[0]][front_pos2[1]] = Air(self.world, front_pos2)
                            else:
                                self.world.field[front_pos[0]][front_pos[1]] = Air(self.world, front_pos)
            front_pos = self.get_rotate_position(self.data["rotate"])
            if self.data["activated"]:
                if self.border(front_pos):
                    if self.world.field[front_pos[0]][front_pos[1]].type != "piston head":
                        self.world.field[self.pos[0]][self.pos[1]] = Air(self.world, self.pos)

    def is_block_connect_with_wire(self, rotate):
        return(self.data["rotate"] != (rotate + 2) % 4)

    def is_block_connect_input(self, rotate):
        return(self.data["rotate"] != (rotate + 2) % 4)

    def get_activated_key(self, rotate):# -|-
        return("activated")

    def get_pushable(self, rotate):
        return(not self.data["activated"])

    def get_rotate_position(self, rotate, dist=1):
        return([self.pos[0] + self.movelist[rotate][0] * dist, self.pos[1] + self.movelist[rotate][1] * dist])

    def get_image(self):
        return(get_image(self.data["activated"] + 2 * (self.type == "sticky piston"), 8 + self.data["rotate"], size=self.world.block_scale))