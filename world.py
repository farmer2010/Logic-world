from image_factory import get_image
import image_factory
from block import Block
import block
import pygame
pygame.init()

def bin_to_dec(bin):
    bin = bin[::-1]
    num = 0
    for i in range(len(bin)):
        num += 2 ** i * int(bin[i])
    return (num)

def dec_to_bin(dec):
    b = ""
    while dec > 0:
        b = str(dec % 2) + b
        dec //= 2
    return(b)

def render_text(text, pos, screen, color=(0, 0, 0), centerx="left", centery="up", font=pygame.font.SysFont(None, 40)):#отрисовка текста на экране
    text_img = font.render(text, True, color)
    text_rect = text_img.get_rect()
    if centerx == "left":
        text_rect.x = pos[0]
    elif centerx == "center":
        text_rect.centerx = pos[0]
    elif centerx == "right":
        text_rect.x = pos[0] - text_img.get_width()
    if centery == "up":
        text_rect.y = pos[1]
    elif centery == "center":
        text_rect.centery = pos[1]
    elif centery == "down":
        text_rect.y = pos[1] - text_img.get_height()
    screen.blit(text_img, text_rect)

class World:
    def __init__(self, w=10, h=10, pos=[0, 0], level_name="level"):
        self.level_name = level_name
        self.w = w
        self.h = h
        self.field = [[None for y in range(h)] for x in range(w)]
        self.field = [[Block(self, (x, y), "air") for y in range(h)] for x in range(w)]
        self.pos = [pos[0] * 40, pos[1] * 40]
        W = pygame.display.Info().current_w
        H = pygame.display.Info().current_h
        self.display_w = W
        self.display_h = H
        self.floor_img = pygame.Surface((W, H))
        for x in range(int(W / 40)):
            for y in range(int(H / 40)):
                if x >= pos[0] and x < pos[0] + self.w and y >= pos[1] and y < pos[1] + self.h:
                    self.floor_img.blit(get_image(1, 0), (x * 40, y * 40))
                else:
                    self.floor_img.blit(get_image(0, 0), (x * 40, y * 40))
        self.change_image()
        self.mousetag = 0
        self.timer = 0
        self.select_rotate = 0
        self.r_tag = 0#нажата ли клафиша r
        self.buttons = pygame.sprite.Group()
        self.is_creative = 1
        self.can_break = 1
        self.block_indexes = {"wire" : 0, "activator" : 1, "block" : 2, "NOT" : 3, "wire box" : 4, "AND" : 5, "XOR" : 6, "diode" : 7, "output" : 8, "glass" : 9, "armored wire" : 10}
        self.block_indexes2 = ["wire", "activator", "block", "NOT", "wire box", "AND", "XOR", "diode", "output", "glass", "armored wire"]
        self.inventory_index = 0
        self.inventory = {"wire" : 9999, "activator" : 9999, "block" : 9999, "NOT" : 9999, "wire box" : 9999, "AND" : 9999, "XOR" : 9999, "diode" : 9999, "armored wire" : 9999, "memory" : 9999, "output" : 9999, "glass" : 9999, "air" : 0}
        self.inventory_names = ["wire", "activator", "block", "NOT", "wire box", "AND", "XOR", "diode", "armored wire", "memory", "output", "glass", "air"]
        #self.load_level("level")

    def update(self, events):
        keys = pygame.key.get_pressed()#проверка нажатий кнопок
        #смена блока "в руке"
        for event in events:
            if event.type == pygame.MOUSEWHEEL:
                if self.inventory_index > len(self.inventory_names) - 2:
                    self.inventory_index = (self.inventory_index - event.y) % len(self.inventory_names)
                else:
                    self.inventory_index -= event.y
                    if self.inventory_index < 0:
                        self.inventory_index = 0
                    elif self.inventory_index > len(self.inventory_names) - 2:
                        self.inventory_index = len(self.inventory_names) - 2
        #смена активного блока посредством курсора
        mousepos = pygame.mouse.get_pos()
        block_index = mousepos[1] // 80
        xborder = mousepos[0] >= self.display_w - 70
        yborder = (block_index < len(self.inventory_names) - 1) and mousepos[1] >= block_index * 80 + 10 and mousepos[1] <= block_index * 80 + 70
        if xborder and yborder:
            if pygame.mouse.get_pressed()[0]:
                self.inventory_index = block_index
        #поворот блока
        if keys[pygame.K_r]:
            if self.r_tag == 0:
                self.select_rotate += 1
                self.select_rotate %= 4
                self.r_tag = 1
        else:
            self.r_tag = 0
        #пипетка
        if keys[pygame.K_q]:
            mousepos = pygame.mouse.get_pos()
            mouse_world_pos = [mousepos[0] - self.pos[0], mousepos[1] - self.pos[1]]
            blockpos = [int(mouse_world_pos[0] / 40), int(mouse_world_pos[1] / 40)]
            if blockpos[0] >= 0 and blockpos[0] < self.w and blockpos[1] >= 0 and blockpos[1] < self.h:
                i = 0
                while self.inventory_names[i] != self.field[blockpos[0]][blockpos[1]].type:
                    i += 1
                if i != None:
                    self.inventory_index = i
            else:
                self.select_block = "air"
        #сохранение уровня
        if keys[pygame.K_F1]:
            self.save_level(self.level_name)
        #загрузка уровня
        if keys[pygame.K_F2]:
            self.load_level(self.level_name)
        #установка и ломание
        if pygame.mouse.get_pressed()[0]:#установка
            mousepos = pygame.mouse.get_pos()
            mouse_world_pos = [mousepos[0] - self.pos[0], mousepos[1] - self.pos[1]]
            blockpos = [int(mouse_world_pos[0] / 40), int(mouse_world_pos[1] / 40)]
            if blockpos[0] >= 0 and blockpos[0] < self.w and blockpos[1] >= 0 and blockpos[1] < self.h and self.can_break and not xborder:
                if self.inventory_names[self.inventory_index] == "glass":
                    if self.is_creative:
                        self.field[blockpos[0]][blockpos[1]].glassed = 1
                        self.change_image()
                else:
                    if self.field[blockpos[0]][blockpos[1]].type == "air":
                        do_set = 1
                        if self.is_creative == 0 and self.inventory[self.inventory_names[self.inventory_index]] == 0:
                            do_set = 0
                        if self.field[blockpos[0]][blockpos[1]].glassed == 0 and do_set:
                            self.timer = 0
                            bl = block.get_block(self, blockpos, self.inventory_names[self.inventory_index])
                            sl = self.inventory_names[self.inventory_index]
                            if sl == "NOT" or sl == "AND" or sl == "XOR" or sl == "diode" or sl == "output":
                                bl.data["rotate"] = self.select_rotate
                            bl.connect_with_armored_wire()
                            self.change_image()
                            self.mousetag = 1
                            if self.is_creative == 0:
                                self.inventory[self.inventory_names[self.inventory_index]] -= 1
                            #------------------------------------
                    elif self.mousetag == 0:#нажатие на блок
                        self.timer = 0
                        self.mousetag = 1
                        self.field[blockpos[0]][blockpos[1]].action()
                        self.change_image()
        else:
           self.mousetag = 0
        #---------------------------------------------------------------------------------------------------------------
        if pygame.mouse.get_pressed()[2]:#ломание
            mousepos = pygame.mouse.get_pos()
            mouse_world_pos = [mousepos[0] - self.pos[0], mousepos[1] - self.pos[1]]
            blockpos = [int(mouse_world_pos[0] / 40), int(mouse_world_pos[1] / 40)]
            if blockpos[0] >= 0 and blockpos[0] < self.w and blockpos[1] >= 0 and blockpos[1] < self.h and self.can_break and not xborder:
                if self.inventory_names[self.inventory_index] == "glass":
                    if self.is_creative:
                        self.field[blockpos[0]][blockpos[1]].glassed = 0
                        self.change_image()
                else:
                    if self.field[blockpos[0]][blockpos[1]].glassed == 0:
                        if self.is_creative == 0:
                            self.inventory[self.field[blockpos[0]][blockpos[1]].type] += 1
                        self.timer = 0
                        self.field[blockpos[0]][blockpos[1]] = Block(self, blockpos, "air")
                        #------------------------------------------------
                        for i in range(4):
                            pos = self.field[blockpos[0]][blockpos[1]].get_rotate_position(i)
                            if self.field[blockpos[0]][blockpos[1]].border(pos):
                                if self.field[pos[0]][pos[1]].type == "armored wire":
                                    self.field[pos[0]][pos[1]].data["connections"][(i + 2) % 4] = 0
                        self.change_image()
        #---------------------------------------------------------------------------------------------------------------
        if self.timer == 0:#обновление карты
            for x in range(self.w):#стираем active и электричество
                for y in range(self.h):
                    self.field[x][y].active = 0
                    if self.field[x][y].type == "wire" or self.field[x][y].type == "output" or self.field[x][y].type == "armored wire":
                        self.field[x][y].data["activated"] = 0
                    elif self.field[x][y].type == "wire box" or self.field[x][y].type == "diode":
                        self.field[x][y].data["activated1"] = 0
                        self.field[x][y].data["activated2"] = 0
            for x in range(self.w):#распространение электричества
                for y in range(self.h):
                    if self.field[x][y].type == "activator" or self.field[x][y].type == "NOT" or self.field[x][y].type == "AND" or self.field[x][y].type == "XOR" or self.field[x][y].type == "memory":
                        if self.field[x][y].data["activated"] == 1:
                            self.field[x][y].update()
            for x in range(self.w):#активация логических вентилей
                for y in range(self.h):
                    if self.field[x][y].type == "NOT" or self.field[x][y].type == "AND" or self.field[x][y].type == "XOR" or self.field[x][y].type == "memory":
                        self.field[x][y].update(self.field[x][y].data, enr=0)
            self.change_image()
        self.timer = 0
        #self.timer += 1
        #if self.timer >= 60:
        #    self.timer = 0
        #
        self.calculate_win()

    def draw(self, screen):
        font = pygame.font.SysFont(None, 25)
        screen.fill((90, 90, 90))
        screen.blit(self.floor_img, [0, 0])#пол
        for x in range(self.w):#блоки
            for y in range(self.h):
                self.field[x][y].draw(screen, self.pos)
        #"тень" от блока в "руке"
        mousepos = pygame.mouse.get_pos()
        mouse_world_pos = [mousepos[0] - self.pos[0], mousepos[1] - self.pos[1]]
        blockpos = [int(mouse_world_pos[0] / 40), int(mouse_world_pos[1] / 40)]
        if blockpos[0] >= 0 and blockpos[0] < self.w and blockpos[1] >= 0 and blockpos[1] < self.h:
            if self.field[blockpos[0]][blockpos[1]].type == "air" or self.inventory_names[self.inventory_index] == "glass":
                if self.inventory_names[self.inventory_index] != "air":
                    select_image = image_factory.get_block_image(self.inventory_names[self.inventory_index], [0, 0, 0, 0], {"activated" : 0, "rotate" : self.select_rotate, "activated1" : 0, "activated2" : 0})
                    select_image.convert_alpha()
                    select_image.set_alpha(90)
                else:
                    select_image = image_factory.get_block_image("air", [], {})
                screen.blit(select_image, (blockpos[0] * 40 + self.pos[0], blockpos[1] * 40 + self.pos[1]))
        #
        if self.inventory_index != len(self.inventory_names) - 1:
            pygame.draw.rect(screen, (255, 255, 0), (self.display_w - 75, self.inventory_index * 80 + 5, 70, 70))
        #
        for i in range(len(self.inventory_names) - 1):
            pygame.draw.rect(screen, (30, 30, 30), (self.display_w - 70, i * 80 + 10, 60, 60))
            pygame.draw.rect(screen, (50, 50, 50), (self.display_w - 65, i * 80 + 15, 50, 50))
            img = image_factory.get_block_image(self.inventory_names[i], [0, 0, 0, 0], {"activated" : 0, "rotate" : 0, "activated1" : 0, "activated2" : 0})
            screen.blit(img, (self.display_w - 60, i * 80 + 20))
            render_text(str(self.inventory[self.inventory_names[i]]), (self.display_w - 10, i * 80 + 45), screen, centerx="right", font=pygame.font.Font("files/font.ttf", 16))

    def change_image(self):
        for x in range(self.w):
            for y in range(self.h):
                self.field[x][y].change_image()

    def save_level(self, name):
        file = open("files/levels/" + name + ".dat", "w")
        txt = ""
        txt += str(self.w) + ";"
        txt += str(self.h) + ";"
        txt += str(int(self.pos[0] / 40)) + ";"
        txt += str(int(self.pos[1] / 40)) + ";"
        glassed = ""
        for x in range(self.w):
            for y in range(self.h):
                glassed += str(self.field[x][y].glassed)
        txt += str(bin_to_dec(glassed)) + ";"
        for i in range(len(self.inventory_names) - 1):
            txt += str(self.block_indexes[self.inventory_names[i]]) + "," + str(self.inventory[self.inventory_names[i]])
            txt += ":"
        txt += ";"
        for x in range(self.w):
            for y in range(self.h):
                if self.field[x][y].type != "air":
                    txt += str(self.block_indexes[self.field[x][y].type]) + ","
                    txt += str(self.field[x][y].pos[0]) + ","
                    txt += str(self.field[x][y].pos[1]) + ","
                    if self.field[x][y].type != "wire box" and self.field[x][y].type != "diode":
                        txt += str(int(self.field[x][y].data["activated"])) + ","
                    if self.field[x][y].type == "NOT" or self.field[x][y].type == "AND" or self.field[x][y].type == "XOR" or self.field[x][y].type == "diode" or self.field[x][y].type == "output":
                        txt += str(self.field[x][y].data["rotate"]) + ","
                    if self.field[x][y].type == "wire box" or self.field[x][y].type == "AND" or self.field[x][y].type == "XOR" or self.field[x][y].type == "diode" or self.field[x][y].type == "memory":
                        txt += str(int(self.field[x][y].data["activated1"])) + ","
                        txt += str(int(self.field[x][y].data["activated2"])) + ","
                    if self.field[x][y].type == "armored wire":
                        for i in range(4):
                            txt += str(int(self.field[x][y].data["connections"][i]))
                        txt += ","
                    if 
                    txt += ":"
        txt += ";"
        file.write(txt)
        file.close()

    def load_level(self, name):
        file = open("files/levels/" + name + ".dat", "r")
        txt = file.readline()
        self.w = int(txt.split(";")[0])
        self.h = int(txt.split(";")[1])
        self.pos[0] = int(txt.split(";")[2]) * 40
        self.pos[1] = int(txt.split(";")[3]) * 40
        pos = [int(txt.split(";")[2]) , int(txt.split(";")[3])]
        file.close()
        W = pygame.display.Info().current_w
        H = pygame.display.Info().current_h
        self.floor_img = pygame.Surface((W, H))
        for x in range(int(W / 40)):
            for y in range(int(H / 40)):
                if x >= pos[0] and x < pos[0] + self.w and y >= pos[1] and y < pos[1] + self.h:
                    self.floor_img.blit(get_image(1, 0), (x * 40, y * 40))
                else:
                    self.floor_img.blit(get_image(0, 0), (x * 40, y * 40))
        self.field = [[Block(self, (x, y), "air") for y in range(self.h)] for x in range(self.w)]
        #
        inv = txt.split(";")[5].split(":")
        self.inventory = {"air" : 0}
        self.inventory_names = []
        for i in range(len(inv) - 1):
            invi = inv[i].split(",")
            self.inventory_names.append(self.block_indexes2[int(invi[0])])
            self.inventory[self.block_indexes2[int(invi[0])]] = int(invi[1])
        self.inventory_names.append("air")
        #
        blocks = txt.split(";")[6].split(":")
        for i in range(len(blocks)):
            bl = blocks[i].split(",")#данные блока
            if bl != [""]:
                new_block = block.get_block(self, (int(bl[1]), int(bl[2])), self.block_indexes2[int(bl[0])])
                if int(bl[0]) == 0:
                    new_block.data["activated"] = int(bl[3])
                elif int(bl[0]) == 1:
                    new_block.data["activated"] = int(bl[3])
                elif int(bl[0]) == 3:
                    new_block.data["activated"] = int(bl[3])
                    new_block.data["rotate"] = int(bl[4])
                elif int(bl[0]) == 4:
                    new_block.data["activated1"] = int(bl[3])
                    new_block.data["activated2"] = int(bl[4])
                elif int(bl[0]) == 5 or int(bl[0]) == 6:
                    new_block.data["activated"] = int(bl[3])
                    new_block.data["rotate"] = int(bl[4])
                    new_block.data["activated1"] = int(bl[5])
                    new_block.data["activated2"] = int(bl[6])
                elif int(bl[0]) == 7:
                    new_block.data["rotate"] = int(bl[3])
                    new_block.data["activated1"] = int(bl[4])
                    new_block.data["activated2"] = int(bl[5])
                elif int(bl[0]) == 8:
                    new_block.data["activated"] = int(bl[3])
                    new_block.data["rotate"] = int(bl[4])
                elif int(bl[0]) == 10:
                    new_block.data["activated"] = int(bl[3])
                    new_block.data["connections"] = [bl[4][i] == "1" for i in range(4)]
        #
        glass = dec_to_bin(int(txt.split(";")[4]))
        glass = ("0" * (self.w * self.h - len(glass))) + glass
        for x in range(self.w):
            for y in range(self.h):
                self.field[x][y].glassed = int(glass[x * self.h + y])
        self.change_image()

    def calculate_win(self):
        win_list = []
        for x in range(self.w):
            for y in range(self.h):
                if self.field[x][y].type == "output":
                    win_list.append(self.field[x][y].data["activated"])
        if sum(win_list) == len(win_list) and len(win_list) > 0:
            pass