from block import Block

class LogicGate(Block):
    def __init__(self, world, pos, type, glassed=0, data=None):
        Block.__init__(self, world, pos, type, glassed, data)
        for i in range(4):
            pos = self.get_rotate_position(i)
            if self.border(pos):
                if self.world.field[pos[0]][pos[1]].type == "armored wire" and self.world.field[pos[0]][pos[1]].is_block_connect_with_wire(i) and self.is_block_connect_with_wire((i + 2) % 4):
                    self.world.field[pos[0]][pos[1]].data["connections"][(i + 2) % 4] = 1

    def update(self, data={}, enr=1):
        if not enr:
            left_pos = self.get_rotate_position((self.data["rotate"] - 1) % 4)
            right_pos = self.get_rotate_position((self.data["rotate"] + 1) % 4)
            in1 = 0
            in2 = 0
            # левый вход
            if self.border(left_pos):
                r = (self.data["rotate"] - 1) % 4
                left_block = self.world.field[left_pos[0]][left_pos[1]]
                if left_block.type == "wire" or left_block.type == "activator":#считываем сигнал с провода или активатора
                    in1 = left_block.data["activated"]
                elif left_block.type == "wire box":#считываем сигнал с распределительной коробки
                    if r == 0 or r == 2:#вверху - внизу
                        in1 = left_block.data["activated2"]
                    elif r == 3 or r == 1:#влево - вправо
                        in1 = left_block.data["activated1"]
                elif (left_block.type == "NOT" or left_block.type == "AND" or left_block.type == "XOR") and left_block.data["rotate"] == (r + 2) % 4:#считываем сигнал с логических вентилей
                    in1 = left_block.data["activated"]
                elif left_block.type == "diode" and left_block.data["rotate"] == (r + 2) % 4:#считываем сигнал с диода
                    in1 = left_block.data["activated2"]
                elif left_block.type == "armored wire" and left_block.data["connections"][(r + 2) % 4]:#считываем сигнал с защищенного провода
                    in1 = left_block.data["activated"]
            #правый вход
            if self.border(right_pos):
                r = (self.data["rotate"] + 1) % 4
                right_block = self.world.field[right_pos[0]][right_pos[1]]
                if right_block.type == "wire" or right_block.type == "activator":#считываем сигнал с провода или активатора
                    in2 = right_block.data["activated"]
                elif right_block.type == "wire box":#считываем сигнал с распределительной коробки
                    if r == 0 or r == 2:#вверху - внизу
                        in2 = right_block.data["activated2"]
                    elif r == 3 or r == 1:  # влево - вправо
                        in2 = right_block.data["activated1"]
                elif (right_block.type == "NOT" or right_block.type == "AND" or right_block.type == "XOR") and right_block.data["rotate"] == (r + 2) % 4:#считываем сигнал с логических вентилей
                    in2 = right_block.data["activated"]
                elif right_block.type == "diode" and right_block.data["rotate"] == (r + 2) % 4:#считываем сигнал с диода
                    in2 = right_block.data["activated2"]
                elif right_block.type == "armored wire" and right_block.data["connections"][(r + 2) % 4]:#считываем сигнал с защищенного провода
                    in2 = right_block.data["activated"]
            #активация
            if self.type == "AND":
                self.data["activated"] = in1 and in2
                self.active = in1 and in2
            elif self.type == "XOR":
                self.data["activated"] = in1 ^ in2
                self.active = in1 ^ in2
            self.data["activated1"] = in1
            self.data["activated2"] = in2
        #распространение сигнала
        front_pos = self.get_rotate_position(self.data["rotate"])
        if self.border(front_pos):
            front_block = self.world.field[front_pos[0]][front_pos[1]]
            if enr and front_block.active == 0 and self.data["activated"]:#если можно передать сигнал вперед
                if front_block.type == "wire" or front_block.type == "armored wire" or front_block.type == "output":#если передаем сигнал в провод
                    front_block.update({"rotate": self.data["rotate"]})
                elif front_block.type == "wire box":#если передаем сигнал в распределитель
                    if self.data["rotate"] == 0 or self.data["rotate"] == 2:#вверх - вниз
                        front_block.data["activated2"] = 1
                        front_block.update({"rotate": self.data["rotate"]})
                    elif self.data["rotate"] == 1 or self.data["rotate"] == 3:#влево - вправо
                        front_block.data["activated1"] = 1
                        front_block.update({"rotate": self.data["rotate"]})

    def is_block_connect_with_wire(self, rotate):
        print(self.data)
        return(self.data["rotate"] != rotate)