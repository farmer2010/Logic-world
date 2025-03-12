from block import Block

class WireBox(Block):
    def __init__(self, world, pos, glassed=0, data=None):
        Block.__init__(self, world, pos, "wire box", glassed, data)

    def update(self, data={}):
        if data["rotate"] == 1 or data["rotate"] == 3:#горизонтальный провод
            self.data["activated1"] = 1
        elif data["rotate"] == 0 or data["rotate"] == 2:#вертикальный провод
            self.data["activated2"] = 1
        pos = self.get_rotate_position(data["rotate"])
        #
        if self.border(pos):#распространение сигнала
            b = self.world.field[pos[0]][pos[1]]
            if (b.type == "wire" or b.type == "wire box" or b.type == "diode" or b.type == "output" or b.type == "armored wire") and b.active == 0:
                b.update({"rotate": data["rotate"]})

    def is_block_connect_with_wire(self, rotate):
        return(1)