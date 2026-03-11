from input_manager import *
from blocks import *
from button import *
from text_box import *
from text_label import *
from radiobutton import *
import image_factory
import pygame
pygame.init()

W = pygame.display.Info().current_w
H = pygame.display.Info().current_h
font16 = pygame.font.Font("files/Better VCR 6.1.ttf", 16)
font_text = pygame.font.Font("files/Better VCR 6.1.ttf", 16)
ocolor = (128, 128, 128)

inv_original = {
    "wire" : 9999,
    "armored wire": 9999,
    "wire box": 9999,
    "diode": 9999,
    "energy block": 9999,
    "activator" : 9999,
    "button": 9999,
    "NOT" : 9999,
    "AND" : 9999,
    "XOR" : 9999,
    "memory": 9999,
    "sensor": 9999,
    "output" : 9999,
    "glass" : 9999,
    "block": 9999,
    "piston" : 9999,
    "sticky piston" : 9999,
    "no pushable" : 9999,
}#все блоки в игре в количестве 9999

def change_menu(self, menu):
    self.menu = menu
def mainmenu(main):
    from main_menu import MainMenu
    main.menu = MainMenu(main)
def selectlevelmenu(main):
    from select_level import SelectLevel
    main.menu = SelectLevel(main)
def resise(self, w, h):
    try:
        self.edit_buttons[2].text = str(w)
        self.edit_buttons[3].text = str(h)
        self.w = w
        self.h = h
        self.change_floor_image()
        f = [[None for y in range(self.h)] for x in range(self.w)]
        for x in range(self.w):
            for y in range(self.h):
                if x < len(self.field) and y < len(self.field[0]):
                    f[x][y] = self.field[x][y]
        self.field = f
        self.blocks = []
        for x in range(self.w):
            for y in range(self.h):
                if self.field[x][y] == None:
                    self.field[x][y] = Air(self, (x, y))
                elif self.field[x][y].type != "air":
                    self.blocks.append(self.field[x][y])
        self.change_image()
    except Exception as ex:
        print(ex, w, h)
def change_block_scale(self, b):
    try:
        self.block_scale = b
        self.change_floor_image()
    except Exception as ex:
        print(ex, b)
    self.change_image()

class World:
    def __init__(self, main, w=10, h=10, block_scale=20, is_creative=1, number=0):
        W = pygame.display.Info().current_w
        H = pygame.display.Info().current_h
        self.display_w = W
        self.display_h = H
        self.main = main
        self.w = w
        self.h = h
        self.block_scale = block_scale
        self.field = [[None for y in range(h)] for x in range(w)]
        self.field = [[Air(self, (x, y)) for y in range(h)] for x in range(w)]
        self.blocks = []
        self.change_floor_image()
        self.change_image()
        self.timer = 0
        self.number = number
        self.menu = "game"
        self.select_rotate = 0
        self.buttons = pygame.sprite.Group()
        self.is_creative = is_creative
        self.can_break = 1
        self.win_timer = -1
        self.test_mode = 0
        self.block_indexes = {
            "wire" : 0,
            "activator" : 1,
            "block" : 2,
            "NOT" : 3,
            "wire box" : 4,
            "AND" : 5,
            "XOR" : 6,
            "diode" : 7,
            "output" : 8,
            "glass" : 9,
            "armored wire" : 10,
            "memory" : 11,
            "sensor" : 12,
            "energy block" : 13,
            "button" : 14,
            "piston" : 15,
            "piston head" : 16,
            "no pushable" : 17,
            "sticky piston" : 18
        }#для сохранения/загрузки
        self.inventory = inv_original.copy()
        self.creative_inventory_for_save = {
            "wire": [1, 9999],
            "armored wire": [1, 9999],
            "wire box": [1, 9999],
            "diode": [1, 9999],
            "energy block": [1, 9999],
            "activator": [1, 9999],
            "button": [1, 9999],
            "NOT": [1, 9999],
            "AND": [1, 9999],
            "XOR": [1, 9999],
            "memory": [1, 9999],
            "sensor": [1, 9999],
            "output": [1, 9999],
            "glass": [1, 9999],
            "block": [1, 9999],
            "piston": [1, 9999],
            "sticky piston": [1, 9999],
            "no pushable": [1, 9999],
        }
        self.creative_select_block_index = 0
        self.hand = ["wire", "button", "activator", "NOT", "AND", "XOR", "memory", "wire box", "diode", "armored wire", "output", "glass", "air"]
        self.input_manager = input_manager
        self.hand_index = len(self.hand) - 1
        #
        if self.is_creative:
            self.buttons = []
            self.buttons.append(get_button(720, 400, 480, 40, "BACK TO GAME", font_size=16, onrelease=change_menu, onrelease_params=[self, "game"]))
            self.buttons.append(get_button(720, 450, 480, 40, "EDIT", font_size=16, onrelease=change_menu, onrelease_params=[self, "edit"]))
            self.buttons.append(get_text_box(720, 500, 480, 40, "", font=font16))
            self.buttons.append(get_button(720, 550, 235, 40, "SAVE", font_size=16, onrelease=lambda s, t: s.save_level(t.text), onrelease_params=[self, self.buttons[2]]))
            self.buttons.append(get_button(965, 550, 235, 40, "LOAD", font_size=16, onrelease=lambda s, t: s.load_level(t.text), onrelease_params=[self, self.buttons[2]]))
            self.buttons.append(get_button(720, 600, 480, 40, "QUIT TO MENU", font_size=16, onrelease=mainmenu, onrelease_params=[self.main]))
            #
            self.edit_buttons = []
            self.edit_buttons.append(get_button(720, 400, 480, 40, "BACK TO MENU", font_size=16, onrelease=change_menu, onrelease_params=[self, "ESC"]))
            self.edit_buttons.append(get_text_box(870, 450, 85, 40, str(self.block_scale), font=font16))#block scale
            self.edit_buttons.append(get_text_box(750, 500, 205, 40, str(self.w), font=font16))#w
            self.edit_buttons.append(get_text_box(995, 500, 205, 40, str(self.h), font=font16))#h
            self.edit_buttons.append(TextLabel("W:", (720, 520), font_color=(0, 0, 0), font=font_text, center=(0, 0.5), font_alpha=0, outline_size=1, outline_color=ocolor))
            self.edit_buttons.append(TextLabel("H:", (965, 520), font_color=(0, 0, 0), font=font_text, center=(0, 0.5), font_alpha=0, outline_size=1, outline_color=ocolor))
            self.edit_buttons.append(TextLabel("BLOCK SCALE:", (720, 470), font_color=(0, 0, 0), font=font_text, center=(0, 0.5), font_alpha=0, outline_size=1, outline_color=ocolor))
            self.edit_buttons.append(get_button(965, 450, 235, 40, "CHANGE", font_size=16, onrelease=lambda self, b: change_block_scale(self, int(b.text)), onrelease_params=[self, self.edit_buttons[1]]))
            self.edit_buttons.append(get_button(720, 550, 235, 40, "CUT", font_size=16, onrelease=change_menu, onrelease_params=[self, "ESC"]))
            self.edit_buttons.append(get_button(965, 550, 235, 40, "FULL", font_size=16, onrelease=lambda self: resise(self, self.display_w // self.block_scale, self.display_h // self.block_scale), onrelease_params=[self]))
            self.edit_buttons.append(get_button(720, 600, 480, 40, "RESISE", font_size=16, onrelease=lambda self, w, h: resise(self, int(w.text), int(h.text)), onrelease_params=[self, self.edit_buttons[2], self.edit_buttons[3]]))
            self.edit_buttons.append(RadioButton((720, 650, 40, 40), text="CAN BREAK BLOCKS", selected=1, font=font_text, outline_size=1, outline_color=(128, 128, 128)))
            self.edit_buttons.append(get_button(720, 700, 480, 40, "INVENTORY", font_size=16, onrelease=change_menu, onrelease_params=[self, "edit inventory"]))
            #
            self.edit_inv_buttons = []
            self.edit_inv_buttons.append(get_button(10, 10, 480, 40, "<- BACK", font_size=16, onrelease=change_menu, onrelease_params=[self, "edit"]))
            self.edit_inv_buttons.append(get_text_box(670, 100, 200, 40, "9999", font=font16))#count blocks
            self.edit_inv_buttons.append(TextLabel("COUNT:", (660, 120), font_color=(0, 0, 0), font=font_text, center=(1, 0.5), font_alpha=0, outline_size=1, outline_color=ocolor))
            self.edit_inv_buttons.append(RadioButton((670, 50, 40, 40), text="INCLUDE", selected=1, font=font_text, outline_size=1, outline_color=(128, 128, 128)))
        else:
            self.buttons = []
            self.buttons.append(get_button(720, 400, 480, 40, "BACK TO GAME", font_size=16, onrelease=change_menu, onrelease_params=[self, "game"]))
            self.buttons.append(get_button(720, 450, 480, 40, "QUIT TO MENU", font_size=16, onrelease=mainmenu, onrelease_params=[self.main]))

    def update(self, events):
        self.input_manager.update(events)
        #
        if self.win_timer > 0:
            self.win_timer -= 1
        if self.win_timer == 0:
            self.win()
        #
        if self.menu == "game":
            #смена блока "в руке"
            y = self.input_manager.get_mousewheel()
            if self.hand_index > len(self.hand) - 2:
                self.hand_index = (self.hand_index - y) % len(self.hand)
            else:
                self.hand_index -= y
                if self.hand_index < 0:
                    self.hand_index = 0
                elif self.hand_index > len(self.hand) - 2:
                    self.hand_index = len(self.hand) - 2
            #смена активного блока посредством курсора
            mousepos = pygame.mouse.get_pos()
            block_index = mousepos[1] // 80
            xborder = mousepos[0] >= self.display_w - 80
            yborder = (block_index < len(self.hand) - 1) and mousepos[1] >= block_index * 80 + 10 and mousepos[1] <= block_index * 80 + 70
            if self.input_manager.get_mouse(0):
                if xborder and yborder:
                    self.hand_index = block_index
            #поворот блока
            if self.input_manager.get_key("R"):
                mousepos = pygame.mouse.get_pos()
                mouse_world_pos = [mousepos[0] - self.pos[0], mousepos[1] - self.pos[1]]
                blockpos = [int(mouse_world_pos[0] / self.block_scale), int(mouse_world_pos[1] / self.block_scale)]
                if blockpos[0] >= 0 and blockpos[0] < self.w and blockpos[1] >= 0 and blockpos[1] < self.h and not xborder:
                    if "rotate" in self.field[blockpos[0]][blockpos[1]].data:
                        self.field[blockpos[0]][blockpos[1]].data["rotate"] += 1
                        self.field[blockpos[0]][blockpos[1]].data["rotate"] %= 4
                    elif "rotate" in get_block_params(self.hand[self.hand_index]):
                        self.select_rotate += 1
                        self.select_rotate %= 4
                else:
                    if "rotate" in get_block_params(self.hand[self.hand_index]):
                        self.select_rotate += 1
                        self.select_rotate %= 4
            #пипетка
            if self.input_manager.get_key("Q"):
                mousepos = pygame.mouse.get_pos()
                mouse_world_pos = [mousepos[0] - self.pos[0], mousepos[1] - self.pos[1]]
                blockpos = [int(mouse_world_pos[0] / self.block_scale), int(mouse_world_pos[1] / self.block_scale)]
                if blockpos[0] >= 0 and blockpos[0] < self.w and blockpos[1] >= 0 and blockpos[1] < self.h:
                    if self.field[blockpos[0]][blockpos[1]].type in self.hand:
                        i = 0
                        while self.hand[i] != self.field[blockpos[0]][blockpos[1]].type:
                            i += 1
                        if i != None:
                            self.hand_index = i
                    elif self.field[blockpos[0]][blockpos[1]].type in self.inventory.keys():
                        if self.hand_index == len(self.hand) - 1:
                            self.hand_index = 0
                        self.hand[self.hand_index] = self.field[blockpos[0]][blockpos[1]].type
                else:
                    self.select_block = "air"
            #изменение подключений защищенного провода
            con = [self.input_manager.get_key("W"), self.input_manager.get_key("D"), self.input_manager.get_key("S"), self.input_manager.get_key("A")]
            mousepos = pygame.mouse.get_pos()
            mouse_world_pos = [mousepos[0] - self.pos[0], mousepos[1] - self.pos[1]]
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
                if (self.input_manager.mousetag_object[0] == None or self.input_manager.mousetag_object[0] == "action"):
                    mousepos = pygame.mouse.get_pos()
                    mouse_world_pos = [mousepos[0] - self.pos[0], mousepos[1] - self.pos[1]]
                    blockpos = [int(mouse_world_pos[0] / self.block_scale), int(mouse_world_pos[1] / self.block_scale)]
                    if blockpos[0] >= 0 and blockpos[0] < self.w and blockpos[1] >= 0 and blockpos[1] < self.h and not xborder:
                        if self.field[blockpos[0]][blockpos[1]].has_action:
                            self.field[blockpos[0]][blockpos[1]].action()
                            self.input_manager.mousetag_object[0] = "action"
            if not pygame.mouse.get_pressed()[0]:
                self.input_manager.mousetag_object[0] = None
            #
            if pygame.mouse.get_pressed()[0]:#установка
                if (self.input_manager.mousetag_object[0] == None or self.input_manager.mousetag_object[0] == "set"):
                    self.input_manager.mousetag_object[0] = "set"
                    mousepos = pygame.mouse.get_pos()
                    mouse_world_pos = [mousepos[0] - self.pos[0], mousepos[1] - self.pos[1]]
                    blockpos = [int(mouse_world_pos[0] / self.block_scale), int(mouse_world_pos[1] / self.block_scale)]
                    self.set_block(blockpos, xborder)
            else:
                self.input_manager.mousetag_object[0] = None
            #---------------------------------------------------------------------------------------------------------------
            if pygame.mouse.get_pressed()[2]:#ломание
                mousepos = pygame.mouse.get_pos()
                mouse_world_pos = [mousepos[0] - self.pos[0], mousepos[1] - self.pos[1]]
                blockpos = [int(mouse_world_pos[0] / self.block_scale), int(mouse_world_pos[1] / self.block_scale)]
                self.remove_block(blockpos, xborder)
            #---------------------------------------------------------------------------------------------------------------
            #обновление карты
            if self.win_timer == -1:
                self.update_map()
            #открыть инвентарь
            if self.input_manager.get_key("T"):
                self.menu = "select blocks"
                if self.hand_index > len(self.hand) - 2:
                    self.hand_index = 0
            if self.input_manager.get_key("ESC"):
                self.menu = "ESC"
        elif self.menu == "select blocks":
            inv = list(self.inventory.keys())
            if self.input_manager.get_key("T") or self.input_manager.get_key("ESC"):
                self.menu = "game"
            #
            mousepos = pygame.mouse.get_pos()
            block_index = mousepos[1] // 80
            xborder = mousepos[0] >= self.display_w - 70
            yborder = (block_index < len(self.hand) - 1) and mousepos[1] >= block_index * 80 + 10 and mousepos[1] <= block_index * 80 + 70
            if self.input_manager.get_mouse(0):
                if xborder and yborder:
                    self.hand_index = block_index
            #
            blockpos = [(mousepos[0] - (self.display_w - 1040)) // 80, mousepos[1] // 80]
            i = blockpos[1] * 12 + blockpos[0]
            if blockpos[0] >= 0 and blockpos[1] < 12 and self.input_manager.get_mouse(0) and i < len(inv) and not inv[i] in self.hand:
                self.hand[self.hand_index] = inv[i]
        elif self.menu == "ESC":
            if self.input_manager.get_key("ESC"):
                self.menu = "game"
            for b in self.buttons:
                b.update(events)
        elif self.menu == "edit":
            if self.input_manager.get_key("ESC"):
                self.menu = "ESC"
            for b in self.edit_buttons:
                b.update(events)
        elif self.menu == "edit inventory":
            if self.input_manager.get_key("ESC"):
                self.menu = "edit"
            for b in self.edit_inv_buttons:
                b.update(events)
            #
            inv = list(inv_original.keys())
            mousepos = pygame.mouse.get_pos()
            blockpos = [(mousepos[0] - (self.display_w - 1040)) // 80, mousepos[1] // 80]
            i = blockpos[1] * 12 + blockpos[0]
            if blockpos[0] >= 0 and blockpos[1] < 12 and self.input_manager.get_mouse(0) and i < len(inv):
                self.creative_select_block_index = i
                self.edit_inv_buttons[3].selected = self.creative_inventory_for_save[inv[i]][0]
                self.edit_inv_buttons[1].text = str(self.creative_inventory_for_save[inv[i]][1])
            self.creative_inventory_for_save[inv[self.creative_select_block_index]][0] = self.edit_inv_buttons[3].selected
            try:
                self.creative_inventory_for_save[inv[self.creative_select_block_index]][1] = int(self.edit_inv_buttons[1].text)
            except:
                pass

    def update_map(self):
        if self.timer >= 0:#обновление карты
            for bl in self.blocks:#стираем active и электричество
                bl.active = 0
                bl.logic_gate_active = 0
                if bl.type == "wire" or bl.type == "output" or bl.type == "armored wire":
                    bl.data["activated"] = 0
                elif bl.type == "wire box" or bl.type == "diode":
                    bl.data["activated1"] = 0
                    bl.data["activated2"] = 0
            for bl in self.blocks:#распространение электричества
                if bl.has_output:
                    bl.update()
            for bl in self.blocks:#активация логических вентилей
                if bl.is_logic_gate:
                    bl.update(bl.data, enr=0)
            self.change_image()
        #self.timer = 0
        self.timer += 1
        if self.timer >= 60:
            self.timer = 0
        #
        if not self.is_creative and self.timer % 30 == 0:
            self.calculate_win()

    def calculate_win(self):
        win_list = []
        for b in self.blocks:
            if b.type == "output":
                win_list.append(b.data["activated"])
        if sum(win_list) == len(win_list) and len(win_list) > 0:
            self.win_timer = 100

    def win(self):
        file = open("files/save.dat")
        txt = file.readline()
        file.close()
        n = int(txt)
        if n + 1 == self.number:
            file = open("files/save.dat", "w")
            file.write(str(n + 1))
            file.close()
        selectlevelmenu(self.main)

    def set_block(self, blockpos, xborder):
        if blockpos[0] >= 0 and blockpos[0] < self.w and blockpos[1] >= 0 and blockpos[1] < self.h and self.can_break and not xborder:
            if self.hand[self.hand_index] == "glass":
                if self.is_creative:
                    if self.field[blockpos[0]][blockpos[1]].type == "air" and self.field[blockpos[0]][blockpos[1]].glassed == 0:
                        self.blocks.append(self.field[blockpos[0]][blockpos[1]])
                    self.field[blockpos[0]][blockpos[1]].glassed = 1
                    self.change_image()
            elif self.hand[self.hand_index] != "air":
                if self.field[blockpos[0]][blockpos[1]].type == "air":
                    do_set = 1
                    if self.is_creative == 0 and self.inventory[self.hand[self.hand_index]] == 0:
                        do_set = 0
                    if self.field[blockpos[0]][blockpos[1]].glassed == 0 and do_set:
                        self.timer = 0
                        bl = get_block(self, blockpos, self.hand[self.hand_index])
                        self.blocks.append(bl)
                        sl = self.hand[self.hand_index]
                        if "rotate" in get_block_params(sl):
                            bl.data["rotate"] = self.select_rotate
                        bl.connect_with_armored_wire()
                        self.change_image()
                        if self.is_creative == 0:
                            self.inventory[self.hand[self.hand_index]] -= 1

    def remove_block(self, blockpos, xborder):
        if blockpos[0] >= 0 and blockpos[0] < self.w and blockpos[1] >= 0 and blockpos[1] < self.h and self.can_break and not xborder:
            if self.hand[self.hand_index] == "glass":
                if self.is_creative:
                    if self.field[blockpos[0]][blockpos[1]].type == "air" and self.field[blockpos[0]][blockpos[1]].glassed == 1:
                        self.blocks.remove(self.field[blockpos[0]][blockpos[1]])
                    self.field[blockpos[0]][blockpos[1]].glassed = 0
                    self.change_image()
            else:
                if self.field[blockpos[0]][blockpos[1]].glassed == 0:
                    self.timer = 0
                    if self.field[blockpos[0]][blockpos[1]].type != "air":
                        self.blocks.remove(self.field[blockpos[0]][blockpos[1]])
                        if self.is_creative == 0 and self.field[blockpos[0]][blockpos[1]].type in self.inventory:
                            self.inventory[self.field[blockpos[0]][blockpos[1]].type] += 1
                    self.field[blockpos[0]][blockpos[1]] = Air(self, blockpos)
                    # ------------------------------------------------
                    for i in range(4):
                        pos = self.field[blockpos[0]][blockpos[1]].get_rotate_position(i)
                        if self.field[blockpos[0]][blockpos[1]].border(pos):
                            if self.field[pos[0]][pos[1]].type == "armored wire":
                                self.field[pos[0]][pos[1]].data["connections"][(i + 2) % 4] = 0
                    self.change_image()

    def draw(self, screen):
        font = pygame.font.SysFont(None, 25)
        screen.fill((90, 90, 90))
        screen.blit(self.floor_img, [0, 0])#пол
        for bl in self.blocks:#блоки
            bl.draw(screen, self.pos)
        if self.menu == "game":
            #"тень" от блока в "руке"
            mousepos = pygame.mouse.get_pos()
            mouse_world_pos = [mousepos[0] - self.pos[0], mousepos[1] - self.pos[1]]
            blockpos = [int(mouse_world_pos[0] / self.block_scale), int(mouse_world_pos[1] / self.block_scale)]
            if blockpos[0] >= 0 and blockpos[0] < self.w and blockpos[1] >= 0 and blockpos[1] < self.h:
                if self.field[blockpos[0]][blockpos[1]].type == "air" or self.hand[self.hand_index] == "glass":
                    if self.hand[self.hand_index] != "air":
                        select_image = image_factory.get_block_image(self.hand[self.hand_index], [0, 0, 0, 0], {"activated" : 0, "rotate" : self.select_rotate, "activated1" : 0, "activated2" : 0}, size=self.block_scale)
                        select_image.convert_alpha()
                        select_image.set_alpha(90)
                    else:
                        select_image = image_factory.get_block_image("air", [], {}, size=self.block_scale)
                    screen.blit(select_image, (blockpos[0] * self.block_scale + self.pos[0], blockpos[1] * self.block_scale + self.pos[1]))
            #
            if self.hand_index != len(self.hand) - 1:
                pygame.draw.rect(screen, (255, 255, 0), (self.display_w - 75, self.hand_index * 80 + 5, 70, 70))
            #
            for i in range(len(self.hand) - 1):
                pygame.draw.rect(screen, (20, 20, 20), (self.display_w - 70, i * 80 + 10, 60, 60))
                pygame.draw.rect(screen, (50, 50, 50), (self.display_w - 65, i * 80 + 15, 50, 50))
                img = image_factory.get_block_image(self.hand[i], [0, 0, 0, 0], {"activated" : 0, "rotate" : 0, "activated1" : 0, "activated2" : 0})
                screen.blit(img, (self.display_w - 60, i * 80 + 20))
                render_text(str(self.inventory[self.hand[i]]), (self.display_w - 10, i * 80 + 45), screen, center=(1, 0), font=pygame.font.Font("files/font.ttf", 16))
        elif self.menu == "select blocks":
            if self.hand_index != len(self.hand) - 1:
                pygame.draw.rect(screen, (255, 255, 0), (self.display_w - 75, self.hand_index * 80 + 5, 70, 70))
            for i in range(len(self.hand) - 1):
                pygame.draw.rect(screen, (20, 20, 20), (self.display_w - 70, i * 80 + 10, 60, 60))
                pygame.draw.rect(screen, (50, 50, 50), (self.display_w - 65, i * 80 + 15, 50, 50))
                img = image_factory.get_block_image(self.hand[i], [0, 0, 0, 0], {"activated": 0, "rotate": 0, "activated1": 0, "activated2": 0})
                screen.blit(img, (self.display_w - 60, i * 80 + 20))
                render_text(str(self.inventory[self.hand[i]]), (self.display_w - 10, i * 80 + 45), screen, center=(1, 0), font=pygame.font.Font("files/font.ttf", 16))
            mousepos = pygame.mouse.get_pos()
            inv = list(self.inventory.keys())
            for x in range(12):
                for y in range(12):
                    i = y * 12 + x
                    if i < len(inv):
                        if (mousepos[0] - (self.display_w - 1040)) // 80 == x and mousepos[1] // 80 == y:
                            pygame.draw.rect(screen, (40, 40, 40), (self.display_w - 1030 + x * 80, y * 80 + 10, 60, 60))
                        else:
                            pygame.draw.rect(screen, (20, 20, 20), (self.display_w - 1030 + x * 80, y * 80 + 10, 60, 60))
                        pygame.draw.rect(screen, (50, 50, 50), (self.display_w - 1025 + x * 80, y * 80 + 15, 50, 50))
                        img = image_factory.get_block_image(inv[i], [0, 0, 0, 0], {"activated": 0, "rotate": 0, "activated1": 0, "activated2": 0})
                        screen.blit(img, (self.display_w - 1020 + x * 80, y * 80 + 20))
                        if inv[i] in self.hand:
                            img2 = pygame.Surface((50, 50))
                            img2.set_alpha(128)
                            screen.blit(img2, (self.display_w - 1025 + x * 80, y * 80 + 15))
        elif self.menu == "ESC":
            for b in self.buttons:
                b.draw(screen)
        elif self.menu == "edit":
            for b in self.edit_buttons:
                b.draw(screen)
        elif self.menu == "edit inventory":
            for b in self.edit_inv_buttons:
                b.draw(screen)
            #
            mousepos = pygame.mouse.get_pos()
            inv = list(self.inventory.keys())
            pygame.draw.rect(screen, (255, 255, 0), (self.display_w - 1035 + (self.creative_select_block_index % 12) * 80, (self.creative_select_block_index // 12) * 80 + 5, 70, 70))
            #
            for x in range(12):
                for y in range(12):
                    i = y * 12 + x
                    if i < len(inv):
                        if (mousepos[0] - (self.display_w - 1040)) // 80 == x and mousepos[1] // 80 == y:
                            pygame.draw.rect(screen, (40, 40, 40), (self.display_w - 1030 + x * 80, y * 80 + 10, 60, 60))
                        else:
                            pygame.draw.rect(screen, (20, 20, 20), (self.display_w - 1030 + x * 80, y * 80 + 10, 60, 60))
                        pygame.draw.rect(screen, (50, 50, 50), (self.display_w - 1025 + x * 80, y * 80 + 15, 50, 50))
                        img = image_factory.get_block_image(inv[i], [0, 0, 0, 0], {"activated": 0, "rotate": 0, "activated1": 0, "activated2": 0})
                        screen.blit(img, (self.display_w - 1020 + x * 80, y * 80 + 20))
                        if self.creative_inventory_for_save[inv[i]][0] == 0:
                            img2 = pygame.Surface((50, 50))
                            img2.set_alpha(128)
                            screen.blit(img2, (self.display_w - 1025 + x * 80, y * 80 + 15))
                        c = self.creative_inventory_for_save[inv[i]][1]
                        render_text(str(c), (self.display_w - 970 + x * 80, y * 80 + 65), screen, center=(1, 1), font=pygame.font.Font("files/font.ttf", 16))
        #
        #анимация надписи при победе
        #
        if self.win_timer > 70:
            render_text("YOU WIN!", (W / 2, H / 2), screen, center=(0.5, 0.5), font=pygame.font.Font("files/Better VCR 6.1.ttf", 192),
                outline_color=ocolor, outline_size=3, alpha=8.5 * (100 - self.win_timer)
            )
        elif self.win_timer > 15:
            render_text("YOU WIN!", (W / 2, H / 2), screen, center=(0.5, 0.5), font=pygame.font.Font("files/Better VCR 6.1.ttf", 192), outline_color=ocolor, outline_size=3)
        elif self.win_timer > 5:
            render_text("YOU WIN!", (W / 2, H / 2), screen, center=(0.5, 0.5), font=pygame.font.Font("files/Better VCR 6.1.ttf", 192),
                outline_color=ocolor, outline_size=3, alpha=25.5 * (self.win_timer - 5)
            )

    def change_image(self):
        for x in range(self.w):
            for y in range(self.h):
                self.field[x][y].change_image()

    def change_floor_image(self):
        self.floor_img = pygame.Surface((W, H))
        self.pos = [int((W / 2 - self.w * self.block_scale / 2) / self.block_scale) * self.block_scale, int((H / 2 - self.h * self.block_scale / 2) / self.block_scale) * self.block_scale]
        for x in range(int(self.display_w / self.block_scale)):
            for y in range(int(self.display_h / self.block_scale)):
                if x >= self.pos[0] / self.block_scale and x < self.pos[0] / self.block_scale + self.w and y >= self.pos[1] / self.block_scale and y < self.pos[1] / self.block_scale + self.h:
                    self.floor_img.blit(get_image(1, 0, size=self.block_scale), (x * self.block_scale, y * self.block_scale))
                else:
                    self.floor_img.blit(get_image(0, 0, size=self.block_scale), (x * self.block_scale, y * self.block_scale))

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
        if self.is_creative:
            inv = list(self.creative_inventory_for_save.keys())
            for i in range(len(inv)):
                if self.creative_inventory_for_save[inv[i]][0]:
                    txt += str(self.block_indexes[inv[i]]) + "," + str(self.creative_inventory_for_save[inv[i]][1])
                    txt += ":"
        else:
            inv = list(self.inventory.keys())
            for i in range(len(inv) - 1):
                txt += str(self.block_indexes[inv[i]]) + "," + str(self.inventory[inv[i]])
                txt += ":"
        txt += ";"
        txt += str(self.block_scale) + ";"
        txt += str(int(self.edit_buttons[11].get_selected())) + ";"
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
        bi2 = list(self.block_indexes.keys())#block indexes 2
        file = open("files/levels/" + name + ".dat", "r")
        txt = file.readline()
        file.close()
        self.w = int(txt.split(";")[0])
        self.h = int(txt.split(";")[1])
        self.block_scale = int(txt.split(";")[4])
        if self.is_creative:
            self.edit_buttons[1].text = str(self.block_scale)
            self.edit_buttons[2].text = str(self.w)
            self.edit_buttons[3].text = str(self.h)
            self.edit_buttons[11].selected = int(txt.split(";")[5])
        else:
            self.can_break = int(txt.split(";")[5])
        self.change_floor_image()
        self.field = [[None for y in range(self.h)] for x in range(self.w)]
        self.field = [[Air(self, (x, y)) for y in range(self.h)] for x in range(self.w)]
        self.blocks = []
        #
        inv = txt.split(";")[3].split(":")
        if self.is_creative:
            self.creative_inventory_for_save = {
                "wire": [0, 9999],
                "armored wire": [0, 9999],
                "wire box": [0, 9999],
                "diode": [0, 9999],
                "energy block": [0, 9999],
                "activator": [0, 9999],
                "button": [0, 9999],
                "NOT": [0, 9999],
                "AND": [0, 9999],
                "XOR": [0, 9999],
                "memory": [0, 9999],
                "sensor": [0, 9999],
                "output": [0, 9999],
                "glass": [0, 9999],
                "block": [0, 9999],
                "piston": [0, 9999],
                "sticky piston": [0, 9999],
                "no pushable": [0, 9999],
            }
            for i in range(len(inv) - 1):
                invi = inv[i].split(",")
                self.creative_inventory_for_save[bi2[int(invi[0])]][0] = 1
                self.creative_inventory_for_save[bi2[int(invi[0])]][1] = int(invi[1])
            #
            ib = list(inv_original.keys())[self.creative_select_block_index]
            self.edit_inv_buttons[3].selected = self.creative_inventory_for_save[ib][0]
            self.edit_inv_buttons[1].text = str(self.creative_inventory_for_save[ib][1])
        else:
            self.inventory = {}
            self.hand = []
            for i in range(len(inv) - 1):
                invi = inv[i].split(",")
                if i < 12:
                    self.hand.append(bi2[int(invi[0])])
                self.inventory[bi2[int(invi[0])]] = int(invi[1])
            self.hand.append("air")
            self.hand_index = len(self.hand) - 1
        #
        blocks = txt.split(";")[6].split(":")
        for i in range(len(blocks)):
            bl = blocks[i].split(",")#данные блока
            if bl != [""]:
                new_block = get_block(self, (int(bl[1]), int(bl[2])), bi2[int(bl[0])])
                self.blocks.append(new_block)
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
                if self.field[x][y].type == "air" and self.field[x][y].glassed:
                    self.blocks.append(self.field[x][y])
        self.change_image()