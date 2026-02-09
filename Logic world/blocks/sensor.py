from blocks.block import Block
from image_factory import *

class Sensor(Block):
    def __init__(self, world, pos, glassed=0, data=None):
        preset_data = {"activated" : 0, "rotate" : 0}
        Block.__init__(self, world, pos, "sensor", glassed, data, preset_data)
        self.is_logic_gate = 1
        self.has_output = 1

    def update(self, data={}, enr=1):
        if not enr:
            behind_pos = self.get_rotate_position((self.data["rotate"] + 2) % 4)
            #вход
            s = self.data["activated"]
            if self.border(behind_pos):
                behind_block = self.world.field[behind_pos[0]][behind_pos[1]]
                if behind_block.get_activated_key((self.data["rotate"] + 2) % 4) != None:
                    if behind_block.logic_gate_active == 0:
                        self.data["activated"] = behind_block.data[behind_block.get_activated_key((self.data["rotate"] + 2) % 4)]
                else:
                    self.data["activated"] = 0
            else:
                self.data["activated"] = 0
            if self.data["activated"] != s:
                self.logic_gate_active = 1
        if enr:
            #распространение сигнала
            front_pos = self.get_rotate_position(self.data["rotate"])
            if self.border(front_pos):
                front_block = self.world.field[front_pos[0]][front_pos[1]]
                if front_block.active == 0 and self.data["activated"] and front_block.is_block_connect_input(self.data["rotate"]):#если можно передать сигнал вперед
                    front_block.update({"rotate": self.data["rotate"]})

    def is_block_connect_with_wire(self, rotate):
        return(self.data["rotate"] == (rotate + 2) % 4)

    def is_block_connect_output(self, rotate):
        return((self.data["rotate"] + 2) % 4 == rotate)

    def get_activated_key(self, rotate):
        return("activated")

    def get_image(self):
        return(get_image(2 + self.data["activated"], 4 + self.data["rotate"], size=self.world.block_scale))