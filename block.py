from random import randint as rand
from image_factory import *
import pygame
pygame.init()

def get_data(type_):
    if type_ == "wire" or type_ == "activator":
        return({"activated" : 0})
    elif type_ == "NOT":
        return({"activated" : 0, "rotate" : 0})
    elif type_ == "wire box":
        return({"activated1" : 0, "activated2" : 0})#горизонтальный, вертикальный
    elif type_ == "AND" or type_ == "XOR":
        return({"activated1" : 0, "activated2" : 0, "activated" : 0, "rotate" : 0})#левый относительно выхода, правый относительно выхода
    else:
        return({})

class Block():
    def __init__(self, world, pos, sftype, glassed=0, data=None):
        self.world = world
        self.pos = pos
        self.type = sftype
        if data == None:
            self.data = get_data(self.type)
        else:
            self.data = data
        self.glassed = glassed
        self.image = pygame.Surface((40, 40))
        self.movelist = [
            [0, -1],
            [1, 0],
            [0, 1],
            [-1, 0]
        ]
        self.active = 0

    def change_image(self):#сменить картинку
        if self.type == "air":#воздух
            self.image.fill((0, 0, 0))
            self.image.set_colorkey((0, 0, 0))
        elif self.type == "wire":#провод
            see = [0, 0, 0, 0]
            for i in range(4):
                pos = self.get_rotate_position(i)
                if self.border(pos):
                    see[i] = self.is_block_connect_with_wire(i)
            self.image = get_wire_image(self.data, see)
        elif self.type == "activator":#активатор
            self.image = get_activator_image(self.data)
        elif self.type == "block":#кирпич
            self.image = get_image(0, 1)
        elif self.type == "NOT":#логический вентиль NOT
            i = 0
            front_pos = self.get_rotate_position(self.data["rotate"])
            if self.border(front_pos):
                i = self.is_block_connect_with_wire(self.data["rotate"])
            self.image = get_NOT_image(self.data, [i, 0, 0, 0])
        elif self.type == "wire box":#распределительная коробка
            self.image = get_wire_box_image(self.data)
        elif self.type == "AND":#логический вентиль AND
            self.image = get_AND_image(self.data)
        elif self.type == "XOR":#логический вентиль XOR
            self.image = get_XOR_image(self.data)
        if self.glassed:
            see = [0, 0, 0, 0]
            for i in range(4):
                pos = self.get_rotate_position(i)
                if self.border(pos):
                    b = self.world.field[pos[0]][pos[1]]
                    if b.glassed:
                        see[i] = 1
            self.image.blit(get_image(2 + see[2] * 2 + see[3], see[0] * 2 + see[1]), (0, 0))

    def draw(self, screen, world_pos):
        screen.blit(self.image, (world_pos[0] + self.pos[0] * 40, world_pos[1] + self.pos[1] * 40))

    def action(self):#нажатие на блок
        if self.type == "activator":
            self.data["activated"] = not self.data["activated"]

    def update(self, data={}, enr=1):#распространение энергии
        if self.type == "NOT":#не
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
            #активация
            self.data["activated"] = not i
            self.active = not i
            #распространение сигнала
            if self.border(front_pos):
                front_block = self.world.field[front_pos[0]][front_pos[1]]
                if enr and front_block.active == 0 and self.data["activated"]:#если можно передать сигнал вперед
                    if front_block.type == "wire":#если передаем сигнал в провод
                        front_block.data["activated"] = self.data["activated"]
                        front_block.update({"rotate" : self.data["rotate"]})
                    elif front_block.type == "wire box":#если передаем сигнал в распределитель
                        if self.data["rotate"] == 0 or self.data["rotate"] == 2:#вверх - вниз
                            front_block.data["activated2"] = self.data["activated"]
                            front_block.update({"rotate" : self.data["rotate"]})
                        elif self.data["rotate"] == 1 or self.data["rotate"] == 3:#влево - вправо
                            front_block.data["activated1"] = self.data["activated"]
                            front_block.update({"rotate" : self.data["rotate"]})
        elif self.type == "AND" or self.type == "XOR":#и, или
            if not enr:
                left_pos = self.get_rotate_position((self.data["rotate"] - 1) % 4)
                right_pos = self.get_rotate_position((self.data["rotate"] + 1) % 4)
                in1 = 0
                in2 = 0
                #левый вход
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
                #правый вход
                if self.border(right_pos):
                    r = (self.data["rotate"] + 1) % 4
                    right_block = self.world.field[right_pos[0]][right_pos[1]]
                    if right_block.type == "wire" or right_block.type == "activator":#считываем сигнал с провода или активатора
                        in2 = right_block.data["activated"]
                    elif right_block.type == "wire box":#считываем сигнал с распределительной коробки
                        if r == 0 or r == 2:#вверху - внизу
                            in2 = right_block.data["activated2"]
                        elif r == 3 or r == 1:#влево - вправо
                            in2 = right_block.data["activated1"]
                    elif (right_block.type == "NOT" or right_block.type == "AND" or right_block.type == "XOR") and right_block.data["rotate"] == (r + 2) % 4:#считываем сигнал с логических вентилей
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
                    if front_block.type == "wire":#если передаем сигнал в провод
                        front_block.data["activated"] = 1
                        front_block.update({"rotate" : self.data["rotate"]})
                    elif front_block.type == "wire box":#если передаем сигнал в распределитель
                        if self.data["rotate"] == 0 or self.data["rotate"] == 2:#вверх - вниз
                            front_block.data["activated2"] = 1
                            front_block.update({"rotate" : self.data["rotate"]})
                        elif self.data["rotate"] == 1 or self.data["rotate"] == 3:#влево - вправо
                            front_block.data["activated1"] = 1
                            front_block.update({"rotate" : self.data["rotate"]})
        elif self.type == "wire box":#распределительная коробка
            if data["rotate"] == 1 or data["rotate"] == 3:#горизонтальный провод
                self.data["activated1"] = 1
            elif data["rotate"] == 0 or data["rotate"] == 2:#вертикальный провод
                self.data["activated2"] = 1
            pos = self.get_rotate_position(data["rotate"])
            if self.border(pos):#распространение сигнала
                b = self.world.field[pos[0]][pos[1]]
                if (b.type == "wire" or b.type == "wire box") and b.active == 0:
                    b.update({"rotate" : data["rotate"]})  
        else:#провод или активатор
            self.active = 1
            self.data["activated"] = 1
            for i in range(4):
                pos = self.get_rotate_position(i)
                if self.border(pos):
                    b = self.world.field[pos[0]][pos[1]]
                    if (b.type == "wire" or b.type == "wire box") and b.active == 0:
                        b.update({"rotate" : i})

    def get_rotate_position(self, rotate):
        return([self.pos[0] + self.movelist[rotate][0], self.pos[1] + self.movelist[rotate][1]])

    def border(self, pos):
        return(pos[0] >= 0 and pos[0] < self.world.w and pos[1] >= 0 and pos[1] < self.world.h)

    def is_block_connect_with_wire(self, rotate):
        pos = self.get_rotate_position(rotate)
        b = self.world.field[pos[0]][pos[1]]
        return(b.type == "wire" or b.type == "activator" or (b.type == "NOT" and (b.data["rotate"] == rotate or (b.data["rotate"] + 2) % 4 == rotate)) or b.type == "wire box" or ((b.type == "AND" or b.type == "XOR") and b.data["rotate"] != rotate))
