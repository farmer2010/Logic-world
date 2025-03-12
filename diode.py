from block import Block

class Diode(Block):
    def __init__(self, world, pos, glassed=0, data=None):
        Block.__init__(self, world, pos, "diode", glassed, data)

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