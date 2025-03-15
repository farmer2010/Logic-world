from block import Block

class NOT(Block):
    def __init__(self, world, pos, glassed=0, data=None):
        Block.__init__(self, world, pos, "NOT", glassed, data)

    def update(self, data={}, enr=1):
        front_pos = self.get_rotate_position(self.data["rotate"])
        behind_pos = self.get_rotate_position((self.data["rotate"] + 2) % 4)
        inp = 0
        #вход
        if self.border(behind_pos):
            behind_block = self.world.field[behind_pos[0]][behind_pos[1]]
            if behind_block.is_block_connect_output((self.data["rotate"] + 2) % 4):
                inp = behind_block.data[behind_block.get_activated_key((self.data["rotate"] + 2) % 4)]
        #активация
        self.data["activated"] = not inp
        self.active = not inp
        #распространение сигнала
        if self.border(front_pos):
            front_block = self.world.field[front_pos[0]][front_pos[1]]
            if enr and front_block.active == 0 and self.data["activated"]:#если можно передать сигнал вперед
                if front_block.type == "wire" or front_block.type == "armored wire" or front_block.type == "output":#если передаем сигнал в провод
                    front_block.update({"rotate": self.data["rotate"]})
                elif front_block.type == "wire box":#если передаем сигнал в распределитель
                    if self.data["rotate"] == 0 or self.data["rotate"] == 2:#вверх - вниз
                        front_block.data["activated2"] = self.data["activated"]
                        front_block.update({"rotate": self.data["rotate"]})
                    elif self.data["rotate"] == 1 or self.data["rotate"] == 3:#влево - вправо
                        front_block.data["activated1"] = self.data["activated"]
                        front_block.update({"rotate": self.data["rotate"]})

    def is_block_connect_with_wire(self, rotate):
        return(self.data["rotate"] == rotate or (self.data["rotate"] + 2) % 4 == rotate)

    def is_block_connect_output(self, rotate):
        return((self.data["rotate"] + 2) % 4 == rotate)

    def is_block_connect_input(self, rotate):
        return(self.data["rotate"] == rotate)

    def connect_with_armored_wire(self):
        for i in range(4):
            pos = self.get_rotate_position(i)
            if self.border(pos):
                if self.world.field[pos[0]][pos[1]].type == "armored wire" and self.world.field[pos[0]][pos[1]].is_block_connect_with_wire(i) and self.is_block_connect_with_wire((i + 2) % 4):
                    self.world.field[pos[0]][pos[1]].data["connections"][(i + 2) % 4] = 1