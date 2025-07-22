from block import Block

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
            if self.border(behind_pos):
                behind_block = self.world.field[behind_pos[0]][behind_pos[1]]
                s = self.data["activated"]
                if behind_block.get_activated_key((self.data["rotate"] + 2) % 4) != None:
                    self.data["activated"] = behind_block.data[behind_block.get_activated_key((self.data["rotate"] + 2) % 4)]
                else:
                    self.data["activated"] = 0
                if self.data["activated"] != s:
                    self.active = 1
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

    def connect_with_armored_wire(self):
        for i in range(4):
            pos = self.get_rotate_position(i)
            if self.border(pos):
                if self.world.field[pos[0]][pos[1]].type == "armored wire" and self.world.field[pos[0]][pos[1]].is_block_connect_with_wire(i) and self.is_block_connect_with_wire((i + 2) % 4):
                    self.world.field[pos[0]][pos[1]].data["connections"][(i + 2) % 4] = 1