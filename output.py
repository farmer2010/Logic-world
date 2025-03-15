from block import Block

class Output(Block):
    def __init__(self, world, pos, glassed=0, data=None):
        preset_data = {"activated" : 0, "rotate" : 0}
        Block.__init__(self, world, pos, "output", glassed, data, preset_data)

    def update(self, data={}):
        if data["rotate"] == self.data["rotate"]:
            self.active = 1
            self.data["activated"] = 1

    def is_block_connect_with_wire(self, rotate):
        return(self.data["rotate"] == rotate)

    def is_block_connect_input(self, rotate):
        return (self.data["rotate"] == rotate)

    def connect_with_armored_wire(self):
        for i in range(4):
            pos = self.get_rotate_position(i)
            if self.border(pos):
                if self.world.field[pos[0]][pos[1]].type == "armored wire" and self.world.field[pos[0]][pos[1]].is_block_connect_with_wire(i) and self.is_block_connect_with_wire((i + 2) % 4):
                    self.world.field[pos[0]][pos[1]].data["connections"][(i + 2) % 4] = 1