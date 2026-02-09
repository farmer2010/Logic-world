from blocks.block import Block
from image_factory import *

class LogicGate(Block):
    def __init__(self, world, pos, type, glassed=0, data=None):
        preset_data = {"activated1" : 0, "activated2" : 0, "activated" : 0, "rotate" : 0}
        Block.__init__(self, world, pos, type, glassed, data, preset_data)
        self.is_logic_gate = 1
        self.has_output = 1

    def update(self, data={}, enr=1):
        if not enr:
            left_pos = self.get_rotate_position((self.data["rotate"] - 1) % 4)
            right_pos = self.get_rotate_position((self.data["rotate"] + 1) % 4)
            in1 = 0
            in2 = 0
            s = self.data["activated"]
            #левый вход
            if self.border(left_pos):
                r = (self.data["rotate"] - 1) % 4
                left_block = self.world.field[left_pos[0]][left_pos[1]]
                if left_block.is_block_connect_output(r) and left_block.logic_gate_active == 0:
                    in1 = left_block.data[left_block.get_activated_key(r)]
            #правый вход
            if self.border(right_pos):
                r = (self.data["rotate"] + 1) % 4
                right_block = self.world.field[right_pos[0]][right_pos[1]]
                if right_block.is_block_connect_output(r) and right_block.logic_gate_active == 0:
                    in2 = right_block.data[right_block.get_activated_key(r)]
            #активация
            if self.type == "AND":
                self.data["activated"] = in1 and in2
                self.active = in1 and in2
            elif self.type == "XOR":
                self.data["activated"] = in1 ^ in2
                self.active = in1 ^ in2
            if self.data["activated"]:
                self.logic_gate_active = 1
            self.data["activated1"] = in1
            self.data["activated2"] = in2
        #распространение сигнала
        if enr:
            front_pos = self.get_rotate_position(self.data["rotate"])
            if self.border(front_pos):
                front_block = self.world.field[front_pos[0]][front_pos[1]]
                if front_block.active == 0 and self.data["activated"] and front_block.is_block_connect_input(self.data["rotate"]):#если можно передать сигнал вперед
                    front_block.update({"rotate": self.data["rotate"]})

    def is_block_connect_with_wire(self, rotate):
        return(self.data["rotate"] != rotate)

    def is_block_connect_output(self, rotate):
        return((self.data["rotate"] + 2) % 4 == rotate)

    def is_block_connect_input(self, rotate):
        return((self.data["rotate"] + 1) % 4 == (rotate + 2) % 4 or (self.data["rotate"] - 1) % 4 == (rotate + 2) % 4)

    def get_activated_key(self, rotate):#-|-
        return("activated")

    def get_image(self):
        if self.type == "AND":
            return(get_image(16 + self.data["activated1"] + self.data["activated2"] * 2, self.data["rotate"], size=self.world.block_scale))
        elif self.type == "XOR":
            return(get_image(16 + self.data["activated1"] + self.data["activated2"] * 2, 4 + self.data["rotate"], size=self.world.block_scale))