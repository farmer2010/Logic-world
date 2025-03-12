from block import Block

class Output(Block):
    def __init__(self, world, pos, glassed=0, data=None):
        Block.__init__(self, world, pos, "output", glassed, data)

    def update(self, data={}):
        if data["rotate"] == self.data["rotate"]:
            self.active = 1
            self.data["activated"] = 1

    def is_block_connect_with_wire(self, rotate):
        return(self.data["rotate"] == rotate)