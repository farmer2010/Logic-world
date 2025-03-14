from block import Block

class ArmoredWire(Block):
    def __init__(self, world, pos, glassed=0, data=None):
        Block.__init__(self, world, pos, "armored wire", glassed, data)
        #---------------------------------------------------------------------------------------------------------------
        see = [0, 0, 0, 0]
        for i in range(4):
            pos = self.get_rotate_position(i)
            if self.border(pos):
                see[i] = self.world.field[pos[0]][pos[1]].is_block_connect_with_wire(i)
        for i in range(4):
            pos = self.get_rotate_position(i)
            if self.border(pos):
                if self.world.field[pos[0]][pos[1]].type == "armored wire" and self.world.field[pos[0]][pos[1]].is_block_connect_with_wire(i) and self.is_block_connect_with_wire((i + 2) % 4):
                    self.world.field[pos[0]][pos[1]].data["connections"][(i + 2) % 4] = 1
        if sum(see) <= 2:
            self.data["connections"] = see.copy()

    def update(self, data={}):
        if self.data["connections"][(data["rotate"] + 2) % 4]:
            self.active = 1
            self.data["activated"] = 1
            for i in range(4):
                pos = self.get_rotate_position(i)
                if self.border(pos) and self.data["connections"][i]:
                    b = self.world.field[pos[0]][pos[1]]
                    if (b.type == "wire" or b.type == "wire box" or b.type == "diode" or b.type == "output" or (b.type == "armored wire" and b.data["connections"][(i + 2) % 4])) and b.active == 0:
                        b.update({"rotate": i})

    def is_block_connect_with_wire(self, rotate):
        return (sum(self.data["connections"]) - self.data["connections"][(rotate + 2) % 4] <= 1)