from block import Block

class Diode(Block):
    def __init__(self, world, pos, glassed=0, data=None):
        preset_data = {"activated1": 0, "activated2": 0, "rotate" : 0}
        Block.__init__(self, world, pos, "diode", glassed, preset_data)

    def update(self, data={}):
        if data["rotate"] == self.data["rotate"]:
            self.active = 1
            self.data["activated1"] = 1
            self.data["activated2"] = 1
            pos = self.get_rotate_position(self.data["rotate"])
            if self.border(pos):
                b = self.world.field[pos[0]][pos[1]]
                if (b.type == "wire" or b.type == "wire box" or b.type == "diode" or b.type == "output" or b.type == "armored wire") and b.active == 0:
                    b.update({"rotate": self.data["rotate"]})
        elif self.data["rotate"] == (data["rotate"] + 2) % 4:
            self.data["activated2"] = 1

    def is_block_connect_with_wire(self, rotate):
        return(self.data["rotate"] == rotate or (self.data["rotate"] + 2) % 4 == rotate)

    def is_block_connect_output(self, rotate):
        return((self.data["rotate"] + 2) % 4 == rotate)

    def is_block_connect_input(self, rotate):
        return(self.data["rotate"] == rotate)

    def get_activated_key(self, rotate):
        return("activated2")

    def connect_with_armored_wire(self):
        for i in range(4):
            pos = self.get_rotate_position(i)
            if self.border(pos):
                if self.world.field[pos[0]][pos[1]].type == "armored wire" and self.world.field[pos[0]][pos[1]].is_block_connect_with_armored_wire(i) and self.is_block_connect_with_wire((i + 2) % 4):
                    self.world.field[pos[0]][pos[1]].data["connections"][(i + 2) % 4] = 1