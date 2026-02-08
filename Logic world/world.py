from farmgui.gui import *
from blocks import *
from blocks.image_factory import *
from utils import *
import pygame
pygame.init()

W = pygame.display.Info().current_w
H = pygame.display.Info().current_h

class World(Panel):
    def __init__(self, rect, w=10, h=10, block_scale=40, creative=1, can_break=1, visible=1):
        Panel.__init__(self, rect, visible=visible)
        self.w = w
        self.h = h
        self.block_scale = block_scale
        self.field = [[None for y in range(h)] for x in range(w)]
        self.field = [[Wire(self, (x, y)) for y in range(h)] for x in range(w)]
        #
        self.pos = [int((W / 2 - self.w * self.block_scale / 2) / self.block_scale), int((H / 2 - self.h * self.block_scale / 2) / self.block_scale)]
        self.fpos = [self.pos[0] * self.block_scale, self.pos[1] * self.block_scale]
        self.background_image = pygame.Surface((W, H))
        for x in range(int(W / self.block_scale)):
            for y in range(int(H / self.block_scale)):
                if x >= self.pos[0] and x < self.pos[0] + self.w and y >= self.pos[1] and y < self.pos[1] + self.h:
                    self.background_image.blit(get_image(1, 0, size=self.block_scale), (x * self.block_scale, y * self.block_scale))
                else:
                    self.background_image.blit(get_image(0, 0, size=self.block_scale), (x * self.block_scale, y * self.block_scale))
        self.change_image()
        #
        self.timer = 0
        self.select_rotate = 0
        #
        self.is_creative = creative
        self.can_break = can_break
        #
        self.block_indexes = {
            "wire": 0,
            "activator": 1,
            "block": 2,
            "NOT": 3,
            "wire box": 4,
            "AND": 5,
            "XOR": 6,
            "diode": 7,
            "output": 8,
            "glass": 9,
            "armored wire": 10,
            "memory": 11,
            "sensor": 12,
            "energy block": 13,
            "button": 14,
            "piston": 15,
            "piston head": 16,
            "no pushable": 17,
            "sticky piston": 18
        }
        self.inventory_block_indexes = {
            "wire": 0,
            "activator": 1,
            "block": 2,
            "NOT": 3,
            "wire box": 4,
            "AND": 5,
            "XOR": 6,
            "diode": 7,
            "output": 8,
            "glass": 9,
            "armored wire": 10,
            "memory": 11,
            "sensor": 12,
            "energy block": 13,
            "button": 14,
            "piston": 15,
            "sticky piston": 16,
            "no pushable": 17
        }
        self.inventory_index = 0
        self.inventory = {"wire": 9999, "activator": 9999, "block": 9999, "NOT": 9999, "wire box": 9999, "AND": 9999,
                          "XOR": 9999, "diode": 9999, "armored wire": 9999, "memory": 9999, "output": 9999,
                          "glass": 9999, "air": 0}
        self.inventory_names = ["wire", "activator", "block", "NOT", "wire box", "AND", "XOR", "diode", "armored wire", "memory", "output", "glass", "air"]
        self.menu = "game"
        self.mousetag_object = None

    def update(self, events):
        #смена блока "в руке"
        y = self.input_manager.get_mousewheel()
        if self.inventory_index > len(self.inventory_names) - 2:
            self.inventory_index = (self.inventory_index - y) % len(self.inventory_names)
        else:
            self.inventory_index -= y
            if self.inventory_index < 0:
                self.inventory_index = 0
            elif self.inventory_index > len(self.inventory_names) - 2:
                self.inventory_index = len(self.inventory_names) - 2
        #смена активного блока посредством курсора
        mousepos = pygame.mouse.get_pos()
        block_index = mousepos[1] // 80
        xborder = mousepos[0] >= W - 80
        yborder = (block_index < len(self.inventory_names) - 1) and mousepos[1] >= block_index * 80 + 10 and mousepos[1] <= block_index * 80 + 70
        if self.get_mouse():
            if xborder and yborder:
                self.inventory_index = block_index
        #поворот блока
        if self.input_manager.get_key("R"):
            mousepos = pygame.mouse.get_pos()
            mouse_world_pos = [mousepos[0] - self.fpos[0], mousepos[1] - self.fpos[1]]
            blockpos = [int(mouse_world_pos[0] / 40), int(mouse_world_pos[1] / 40)]
            if blockpos[0] >= 0 and blockpos[0] < self.w and blockpos[1] >= 0 and blockpos[1] < self.h and not xborder:
                if "rotate" in self.field[blockpos[0]][blockpos[1]].data:
                    self.field[blockpos[0]][blockpos[1]].data["rotate"] += 1
                    self.field[blockpos[0]][blockpos[1]].data["rotate"] %= 4
                elif "rotate" in get_block_params(self.inventory_names[self.inventory_index]):
                    self.select_rotate += 1
                    self.select_rotate %= 4
            else:
                if "rotate" in get_block_params(self.inventory_names[self.inventory_index]):
                    self.select_rotate += 1
                    self.select_rotate %= 4
        #пипетка
        if self.input_manager.get_key("Q"):
            mousepos = pygame.mouse.get_pos()
            mouse_world_pos = [mousepos[0] - self.fpos[0], mousepos[1] - self.fpos[1]]
            blockpos = [int(mouse_world_pos[0] / self.block_scale), int(mouse_world_pos[1] / self.block_scale)]
            if blockpos[0] >= 0 and blockpos[0] < self.w and blockpos[1] >= 0 and blockpos[1] < self.h:
                if self.field[blockpos[0]][blockpos[1]].type in self.inventory_names:
                    i = 0
                    while self.inventory_names[i] != self.field[blockpos[0]][blockpos[1]].type:
                        i += 1
                    if i != None:
                        self.inventory_index = i
                elif self.field[blockpos[0]][blockpos[1]].type in self.inventory_block_indexes.keys():
                    if self.inventory_index == len(self.inventory_names) - 1:
                        self.inventory_index = 0
                    self.inventory_names[self.inventory_index] = self.field[blockpos[0]][blockpos[1]].type
                    self.inventory[self.inventory_index] = 9999
            else:
                self.select_block = "air"
        #изменение подключений защищенного провода
        con = [self.input_manager.get_key("W"), self.input_manager.get_key("D"), self.input_manager.get_key("S"), self.input_manager.get_key("A")]
        mousepos = pygame.mouse.get_pos()
        mouse_world_pos = [mousepos[0] - self.fpos[0], mousepos[1] - self.fpos[1]]
        blockpos = [int(mouse_world_pos[0] / self.block_scale), int(mouse_world_pos[1] / self.block_scale)]
        if blockpos[0] >= 0 and blockpos[0] < self.w and blockpos[1] >= 0 and blockpos[1] < self.h and not xborder:
            bl = self.field[blockpos[0]][blockpos[1]]
            if bl.type == "armored wire":
                for i in range(4):
                    if con[i]:
                        pos = bl.get_rotate_position(i)
                        if bl.data["connections"][i] == 1:
                            bl.data["connections"][i] = 0
                        elif sum(bl.data["connections"]) < 2 and bl.border(pos) and self.field[pos[0]][pos[1]].is_block_connect_with_armored_wire(i):
                            bl.data["connections"][i] = 1
                        bl.connect_armored_wires()
        #нажатие на блок
        if self.input_manager.get_mouse(0):
            if (self.mousetag_object == None or self.mousetag_object == "action"):
                mousepos = pygame.mouse.get_pos()
                mouse_world_pos = [mousepos[0] - self.fpos[0], mousepos[1] - self.fpos[1]]
                blockpos = [int(mouse_world_pos[0] / self.block_scale), int(mouse_world_pos[1] / self.block_scale)]
                if blockpos[0] >= 0 and blockpos[0] < self.w and blockpos[1] >= 0 and blockpos[1] < self.h and not xborder:
                    if self.field[blockpos[0]][blockpos[1]].has_action:
                        self.field[blockpos[0]][blockpos[1]].action()
                        self.mousetag_object = "action"
        if not pygame.mouse.get_pressed()[0]:
            self.mousetag_object = None
        #
        if pygame.mouse.get_pressed()[0]:#установка
            if (self.mousetag_object == None or self.mousetag_object == "set"):
                self.mousetag_object = "set"
                mousepos = pygame.mouse.get_pos()
                mouse_world_pos = [mousepos[0] - self.fpos[0], mousepos[1] - self.fpos[1]]
                blockpos = [int(mouse_world_pos[0] / self.block_scale), int(mouse_world_pos[1] / self.block_scale)]
                self.set_block(blockpos, xborder)
        else:
            self.input_manager.mousetag_object[0] = None
        #---------------------------------------------------------------------------------------------------------------
        if pygame.mouse.get_pressed()[2]:#ломание
            mousepos = pygame.mouse.get_pos()
            mouse_world_pos = [mousepos[0] - self.fpos[0], mousepos[1] - self.fpos[1]]
            blockpos = [int(mouse_world_pos[0] / self.block_scale), int(mouse_world_pos[1] / self.block_scale)]
            self.remove_block(blockpos, xborder)
        #---------------------------------------------------------------------------------------------------------------
        #обновление карты
        self.update_map()
        #открыть инвентарь
        if self.input_manager.get_key("T"):
            self.menu = "select blocks"
            if self.inventory_index > len(self.inventory_names) - 2:
                self.inventory_index = 0
        if self.input_manager.get_key("ESC"):
            self.menu = "ESC"
        #
        #
        #
        if self.menu == "select blocks":
            ibi2 = list(self.inventory_block_indexes.keys())
            if self.input_manager.get_key("T") or self.input_manager.get_key("ESC"):
                self.menu = "game"
            #
            mousepos = pygame.mouse.get_pos()
            block_index = mousepos[1] // 80
            xborder = mousepos[0] >= W - 70
            yborder = (block_index < len(self.inventory_names) - 1) and mousepos[1] >= block_index * 80 + 10 and mousepos[1] <= block_index * 80 + 70
            if self.input_manager.get_mouse(0):
                if xborder and yborder:
                    self.inventory_index = block_index
            #
            blockpos = [(mousepos[0] - (W - 1040)) // 80, mousepos[1] // 80]
            i = blockpos[1] * 12 + blockpos[0]
            if blockpos[0] >= 0 and blockpos[1] < 12 and self.input_manager.get_mouse(0) and i < len(ibi2) and not ibi2[i] in self.inventory_names:
                self.inventory_names[self.inventory_index] = ibi2[i]
                self.inventory[ibi2[i]] = 9999
        elif self.menu == "ESC":
            if self.input_manager.get_key("ESC"):
                self.menu = "game"
            for b in self.buttons:
                b.update(events)
        elif self.menu == "edit":
            if self.input_manager.get_key("ESC"):
                self.menu = "ESC"
            for b in self.edit_buttons:#error
                b.update(events)
        #
        #DRAW
        #
        self.paint()

    def get_mouse(self):
        return(pygame.mouse.get_pressed()[0] and self.mousetag_object == None)

    def update_map(self):
        if self.timer == 0:#обновление карты
            for x in range(self.w):#стираем active и электричество
                for y in range(self.h):
                    self.field[x][y].active = 0
                    self.field[x][y].logic_gate_active = 0
                    if self.field[x][y].type == "wire" or self.field[x][y].type == "output" or self.field[x][y].type == "armored wire":
                        self.field[x][y].data["activated"] = 0
                    elif self.field[x][y].type == "wire box" or self.field[x][y].type == "diode":
                        self.field[x][y].data["activated1"] = 0
                        self.field[x][y].data["activated2"] = 0
            for x in range(self.w):#распространение электричества
                for y in range(self.h):
                    if self.field[x][y].has_output:
                        self.field[x][y].update()
            for x in range(self.w):#активация логических вентилей
                for y in range(self.h):
                    if self.field[x][y].is_logic_gate:
                        self.field[x][y].update(self.field[x][y].data, enr=0)
            self.change_image()
        self.timer = 0
        #self.timer += 1
        #if self.timer >= 60:
        #    self.timer = 0
        #
        self.calculate_win()

    def set_block(self, blockpos, xborder):
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
                        bl = get_block(self, blockpos, self.inventory_names[self.inventory_index])
                        sl = self.inventory_names[self.inventory_index]
                        if "rotate" in get_block_params(sl):
                            bl.data["rotate"] = self.select_rotate
                        bl.connect_with_armored_wire()
                        self.change_image()
                        if self.is_creative == 0:
                            self.inventory[self.inventory_names[self.inventory_index]] -= 1

    def remove_block(self, blockpos, xborder):
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
                    self.field[blockpos[0]][blockpos[1]] = Air(self, blockpos)
                    # ------------------------------------------------
                    for i in range(4):
                        pos = self.field[blockpos[0]][blockpos[1]].get_rotate_position(i)
                        if self.field[blockpos[0]][blockpos[1]].border(pos):
                            if self.field[pos[0]][pos[1]].type == "armored wire":
                                self.field[pos[0]][pos[1]].data["connections"][(i + 2) % 4] = 0
                    self.change_image()

    def paint(self):
        screen = self.get_screen()
        #
        for x in range(self.w):#блоки
            for y in range(self.h):
                self.field[x][y].draw(screen, self.fpos)
        if self.menu == "game":
            #"тень" от блока в "руке"
            mousepos = pygame.mouse.get_pos()
            mouse_world_pos = [mousepos[0] - self.fpos[0], mousepos[1] - self.fpos[1]]
            blockpos = [int(mouse_world_pos[0] / self.block_scale), int(mouse_world_pos[1] / self.block_scale)]
            if blockpos[0] >= 0 and blockpos[0] < self.w and blockpos[1] >= 0 and blockpos[1] < self.h:
                if self.field[blockpos[0]][blockpos[1]].type == "air" or self.inventory_names[self.inventory_index] == "glass":
                    if self.inventory_names[self.inventory_index] != "air":
                        select_image = get_block_image(self.inventory_names[self.inventory_index], [0, 0, 0, 0], {"activated" : 0, "rotate" : self.select_rotate, "activated1" : 0, "activated2" : 0}, size=self.block_scale)
                        select_image.convert_alpha()
                        select_image.set_alpha(90)
                    else:
                        select_image = get_block_image("air", [], {}, size=self.block_scale)
                    screen.blit(select_image, (blockpos[0] * self.block_scale + self.fpos[0], blockpos[1] * self.block_scale + self.fpos[1]))
            #
            if self.inventory_index != len(self.inventory_names) - 1:
                pygame.draw.rect(screen, (255, 255, 0), (W - 75, self.inventory_index * 80 + 5, 70, 70))
            #
            for i in range(len(self.inventory_names) - 1):
                pygame.draw.rect(screen, (20, 20, 20), (W - 70, i * 80 + 10, 60, 60))
                pygame.draw.rect(screen, (50, 50, 50), (W - 65, i * 80 + 15, 50, 50))
                img = get_block_image(self.inventory_names[i], [0, 0, 0, 0], {"activated" : 0, "rotate" : 0, "activated1" : 0, "activated2" : 0})
                screen.blit(img, (W - 60, i * 80 + 20))
                render_text(str(self.inventory[self.inventory_names[i]]), (W - 10, i * 80 + 45), screen, centerx="right", font=pygame.font.Font("files/font.ttf", 16))
            #bl = [pygame.mouse.get_pos()[0] // self.block_scale, pygame.mouse.get_pos()[1] // self.block_scale]
            #render_text(str(bl), pygame.mouse.get_pos(), screen, font=pygame.font.Font("files/font.ttf", 16))
        elif self.menu == "select blocks":
            if self.inventory_index != len(self.inventory_names) - 1:
                pygame.draw.rect(screen, (255, 255, 0), (W - 75, self.inventory_index * 80 + 5, 70, 70))
            for i in range(len(self.inventory_names) - 1):
                pygame.draw.rect(screen, (20, 20, 20), (W - 70, i * 80 + 10, 60, 60))
                pygame.draw.rect(screen, (50, 50, 50), (W - 65, i * 80 + 15, 50, 50))
                img = get_block_image(self.inventory_names[i], [0, 0, 0, 0], {"activated": 0, "rotate": 0, "activated1": 0, "activated2": 0})
                screen.blit(img, (W - 60, i * 80 + 20))
                render_text(str(self.inventory[self.inventory_names[i]]), (W - 10, i * 80 + 45), screen, centerx="right", font=pygame.font.Font("files/font.ttf", 16))
            mousepos = pygame.mouse.get_pos()
            ibi2 = list(self.inventory_block_indexes.keys())
            for x in range(12):
                for y in range(12):
                    i = y * 12 + x
                    if i < len(ibi2):
                        if (mousepos[0] - (W - 1040)) // 80 == x and mousepos[1] // 80 == y:
                            pygame.draw.rect(screen, (40, 40, 40), (W - 1030 + x * 80, y * 80 + 10, 60, 60))
                        else:
                            pygame.draw.rect(screen, (20, 20, 20), (W - 1030 + x * 80, y * 80 + 10, 60, 60))
                        pygame.draw.rect(screen, (50, 50, 50), (W - 1025 + x * 80, y * 80 + 15, 50, 50))
                        img = get_block_image(ibi2[i], [0, 0, 0, 0], {"activated": 0, "rotate": 0, "activated1": 0, "activated2": 0})
                        screen.blit(img, (W - 1020 + x * 80, y * 80 + 20))
                        if ibi2[i] in self.inventory_names:
                            img2 = pygame.Surface((50, 50))
                            img2.set_alpha(128)
                            screen.blit(img2, (W - 1025 + x * 80, y * 80 + 15))
        elif self.menu == "ESC":
            #screen.blit(get_button_image(14, 14, 6), (680, 160))
            for b in self.buttons:
                b.draw(screen)
        elif self.menu == "edit":
            #for b in self.edit_buttons:
            #    b.draw(screen)
            render_text("X:", (720, 340), screen, centery="center", font=pygame.font.Font("files/Better VCR 6.1.ttf", 50), alpha=0)
            render_text("Y:", (1040, 340), screen, centery="center", font=pygame.font.Font("files/Better VCR 6.1.ttf", 50), alpha=0)
            render_text("W:", (720, 540), screen, centery="center", font=pygame.font.Font("files/Better VCR 6.1.ttf", 50), alpha=0)
            render_text("H:", (1040, 540), screen, centery="center", font=pygame.font.Font("files/Better VCR 6.1.ttf", 50), alpha=0)

    def change_image(self):
        for x in range(self.w):
            for y in range(self.h):
                self.field[x][y].change_image()

    def save_level(self, name):
        file = open("files/levels/" + name + ".dat", "w")
        txt = ""
        txt += str(self.w) + ";"
        txt += str(self.h) + ";"
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
                    #
                    for key in self.field[x][y].data:
                        if key != "connections":
                            txt += str(int(self.field[x][y].data[key])) + ","
                        else:
                            for i in range(4):
                                txt += str(int(self.field[x][y].data["connections"][i]))
                            txt += ","
                    txt += ":"
        txt += ";"
        file.write(txt)
        file.close()

    def load_level(self, name):
        W = pygame.display.Info().current_w
        H = pygame.display.Info().current_h
        #
        bi2 = list(self.block_indexes.keys())#block indexes 2
        file = open("files/levels/" + name + ".dat", "r")
        txt = file.readline()
        self.w = int(txt.split(";")[0])
        self.h = int(txt.split(";")[1])
        self.fpos = [int((W / 2 - self.w * 40 / 2) / 40) * 40, int((H / 2 - self.h * 40 / 2) / 40) * 40]
        pos = [self.fpos[0] // self.block_scale, self.fpos[1] // self.block_scale]
        file.close()
        W = pygame.display.Info().current_w
        H = pygame.display.Info().current_h
        self.floor_img = pygame.Surface((W, H))
        for x in range(int(W / 40)):
            for y in range(int(H / 40)):
                if x >= pos[0] and x < pos[0] + self.w and y >= pos[1] and y < pos[1] + self.h:
                    self.floor_img.blit(get_image(1, 0), (x * self.block_scale, y * self.block_scale))
                else:
                    self.floor_img.blit(get_image(0, 0), (x * self.block_scale, y * self.block_scale))
        self.field = [[get_block(self, [x, y], "air") for y in range(self.h)] for x in range(self.w)]
        #
        inv = txt.split(";")[3].split(":")
        self.inventory = {"air" : 0}
        self.inventory_names = []
        for i in range(len(inv) - 1):
            invi = inv[i].split(",")
            self.inventory_names.append(bi2[int(invi[0])])
            self.inventory[bi2[int(invi[0])]] = int(invi[1])
        self.inventory_names.append("air")
        #
        blocks = txt.split(";")[4].split(":")
        for i in range(len(blocks)):
            bl = blocks[i].split(",")#данные блока
            if bl != [""]:
                new_block = get_block(self, (int(bl[1]), int(bl[2])), bi2[int(bl[0])])
                p = get_block_params(bi2[int(bl[0])])
                j = 3
                for p_name in p.keys():
                    if p_name != "connections":
                        new_block.data[p_name] = int(bl[j])
                    else:
                        for o in range(4):
                            new_block.data["connections"][o] = int(bl[j][o])
                    j += 1
        #
        glass = dec_to_bin(int(txt.split(";")[2]))
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
            #win
