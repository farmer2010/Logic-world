from blocks.block import *
from image_factory import *
from blocks.piston_head import PistonHead
from blocks.air import Air

class Piston(Block):
    def __init__(self, world, pos, type, glassed=0, data=None):
        preset_data = {"input" : 0, "activated" : 0, "rotate" : 0, "power" : 12}
        Block.__init__(self, world, pos, type, glassed, data, preset_data)
        self.is_logic_gate = 1

    def update(self, data={}, enr=1):
        if enr == 0:
            if self.data["input"]:
                if self.data["activated"] == 0:
                    push = 0
                    count = self.data["power"]
                    a = 0
                    for i in range(self.data["power"] + 1):
                        pos = self.get_rotate_position(self.data["rotate"], dist=i + 1)
                        if self.border(pos):
                            if self.world.field[pos[0]][pos[1]].get_pushable(self.data["rotate"]) == 0:
                                break
                            if self.world.field[pos[0]][pos[1]].type == "air":
                                a = 1
                                if i > 0:
                                    print(1)
                                    push = 1
                                    count = i
                                break
                        else:
                            break
                    if push:
                        for i in range(count, 0, -1):
                            pos = self.get_rotate_position(self.data["rotate"], dist=i)
                            pos2 = self.get_rotate_position(self.data["rotate"], dist=i + 1)
                            self.world.field[pos2[0]][pos2[1]] = self.world.field[pos[0]][pos[1]]
                            self.world.field[pos2[0]][pos2[1]].pos = pos2
                            self.world.field[pos[0]][pos[1]] = Air(self.world, pos)
                    if a:
                        self.data["activated"] = 1
                        front_pos = self.get_rotate_position(self.data["rotate"])
                        if self.border(front_pos):
                            self.world.field[front_pos[0]][front_pos[1]] = PistonHead(self.world, front_pos, data={"rotate" : self.data["rotate"], "sticky" : "sticky" in self.type})
                            self.world.blocks.append(self.world.field[front_pos[0]][front_pos[1]])
            else:
                if self.data["activated"] == 1:#деактивация
                    self.data["activated"] = 0
                    front_pos = self.get_rotate_position(self.data["rotate"])
                    if self.border(front_pos):
                        if self.type == "piston":#обычный поршень просто удаляет подвижную часть
                            self.world.blocks.remove(self.world.field[front_pos[0]][front_pos[1]])
                            self.world.field[front_pos[0]][front_pos[1]] = Air(self.world, front_pos)
                        else:#липкий поршень удаляет подвижную часть и сдвигает блок перед ней к себе
                            front_pos2 = self.get_rotate_position(self.data["rotate"], dist=2)
                            if self.border(front_pos2) and self.world.field[front_pos2[0]][front_pos2[1]].get_pushable((self.data["rotate"] + 2) % 4):
                                self.world.blocks.remove(self.world.field[front_pos[0]][front_pos[1]])
                                self.world.field[front_pos[0]][front_pos[1]] = self.world.field[front_pos2[0]][front_pos2[1]]
                                self.world.field[front_pos[0]][front_pos[1]].pos = front_pos
                                self.world.field[front_pos2[0]][front_pos2[1]] = Air(self.world, front_pos2)
                            else:
                                self.world.blocks.remove(self.world.field[front_pos[0]][front_pos[1]])
                                self.world.field[front_pos[0]][front_pos[1]] = Air(self.world, front_pos)
            #
            #
            #
            self.data["activated"] = self.data["input"]
            #
            front_pos = self.get_rotate_position(self.data["rotate"])
            if self.data["activated"]:
                if self.border(front_pos):
                    if self.world.field[front_pos[0]][front_pos[1]].type != "piston head":
                        self.world.field[self.pos[0]][self.pos[1]] = Air(self.world, self.pos)
                        self.world.blocks.remove(self)

    def is_block_connect_with_wire(self, rotate):
        return(self.data["rotate"] != (rotate + 2) % 4)

    def is_block_connect_input(self, rotate):
        return(self.data["rotate"] != (rotate + 2) % 4)

    def get_input_activated_key(self, rotate):
        return("input")

    def get_pushable(self, rotate):
        return(not self.data["activated"])

    def get_rotate_position(self, rotate, dist=1):
        return([self.pos[0] + self.movelist[rotate][0] * dist, self.pos[1] + self.movelist[rotate][1] * dist])

    def clear_inputs(self):
        self.data["input"] = 0

    def get_image(self):
        return(get_image(self.data["activated"] + 2 * (self.type == "sticky piston"), 8 + self.data["rotate"], size=self.world.block_scale))