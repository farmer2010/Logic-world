from block import Block

class NOT(Block):
    def __init__(self, world, pos, glassed=0, data=None):
        Block.__init__(self, world, pos, "NOT", glassed, data)

    def update(self, data={}, enr=1):
        front_pos = self.get_rotate_position(self.data["rotate"])
        behind_pos = self.get_rotate_position((self.data["rotate"] + 2) % 4)
        i = 0
        #вход
        if self.border(behind_pos):
            behind_block = self.world.field[behind_pos[0]][behind_pos[1]]
            if behind_block.type == "wire" or behind_block.type == "activator":#считываем сигнал с провода или активатора
                i = behind_block.data["activated"]
            elif (behind_block.type == "NOT" or behind_block.type == "AND" or behind_block.type == "XOR") and behind_block.data["rotate"] == self.data["rotate"]:#считываем сигнал с логических вентилей
                i = behind_block.data["activated"]
            elif behind_block.type == "wire box":#считываем сигнал с распределительной коробки
                if self.data["rotate"] == 0 or self.data["rotate"] == 2:#вверху - внизу
                    i = behind_block.data["activated2"]
                elif self.data["rotate"] == 3 or self.data["rotate"] == 1:#влево - вправо
                    i = behind_block.data["activated1"]
            elif behind_block.type == "diode" and behind_block.data["rotate"] == self.data["rotate"]:#считываем сигнал с диода
                i = behind_block.data["activated2"]
            elif behind_block.type == "armored wire" and behind_block.data["connections"][self.data["rotate"]]:#считываем сигнал с защищенного провода
                i = behind_block.data["activated"]
        #активация
        self.data["activated"] = not i
        self.active = not i
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