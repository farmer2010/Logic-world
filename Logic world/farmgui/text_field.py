from farmgui.image_factory import *
from farmgui.utils import *
from farmgui.component import *
import pygame
pygame.init()

class TextField(Component):
    def __init__(self,
                 rect,
                 text="",
                 font=None,
                 font_name="times new roman",
                 font_size=30,
                 font_color=(0, 0, 0),
                 text_x=10,
                 text_y=10,
                 enabled_symbols=None,
                 disabled_symbols=[],
                 scroll_x=False,
                 scroll_y=False,
                 **kwargs
                 ):
        Component.__init__(self, rect, kwargs.get("center"))
        #
        self.inactive_image = kwargs.get("inactive_image") if kwargs.get("inactive_image") != None else get_text_box_image(self.rect.w, self.rect.h, (90, 90, 90))
        self.hover_image = kwargs.get("hover_image") if kwargs.get("hover_image") != None else get_text_box_image(self.rect.w, self.rect.h, (120, 120, 120))
        self.image = self.inactive_image
        #
        self.text = text
        self.text_lines = []
        self.text_x = text_x
        self.text_y = text_y
        if font == None: font = pygame.font.SysFont(font_name, font_size)
        self.font = font
        self.font_color = font_color
        #
        self.enabled_symbols = enabled_symbols
        self.disabled_symbols = disabled_symbols
        #
        self.timer = 0
        self.cursor = 0
        self.cursor_pos = [0, 0]
        self.mouselast = 0
        self.h = self.font.render("W", 1, self.font_color).get_height()
        self.colors = []
        self.scroll_x = scroll_x
        self.scroll_y = scroll_y
        #
        self.onclick = kwargs.get("onclick")
        self.onclick_params = kwargs.get("onclick_params")
        self.onchange = kwargs.get("onchange")
        self.onchange_params = kwargs.get("onchange_params")
        self.onsubmit = kwargs.get("onsubmit")
        self.onsubmit_params = kwargs.get("onsubmit_params")
        self.color_text = kwargs.get("color_text")
        self.update_text_image()
        if self.color_text != None:
            self.colors = self.color_text(self.text_lines)

    def update(self, events):
        self.timer += 1
        self.timer %= 60
        mousedown = pygame.mouse.get_pressed()[0]
        mousepos = self.get_mousepos()
        mouse_collide = self.collide()
        last_text = self.text
        if mouse_collide:
            if mousedown:
                if self.input_manager.mousetag_object[0] == None:
                    if str(type(self.onclick)) == "<class 'function'>":
                        if self.onclick_params != None:
                            self.onclick(*self.onclick_params)
                        else:
                            self.onclick()
                #
                if self.input_manager.mousetag_object[0] == None:
                    mp = [mousepos[0] - self.rect.x, mousepos[1] - self.rect.y]
                    if mp[1] < self.text_y:
                        self.cursor_pos[1] = 0
                    elif mp[1] > len(self.text_lines) * self.h:
                        self.cursor_pos[1] = len(self.text_lines) - 1
                    else:
                        self.cursor_pos[1] = (mp[1] - self.text_y) // self.h
                    #
                    if mp[0] < self.text_x:
                        self.cursor_pos[0] = 0
                    elif mp[0] > self.font.render(self.text_lines[self.cursor_pos[1]], 1, self.font_color).get_width() + self.text_x:
                        self.cursor_pos[0] = len(self.text_lines[self.cursor_pos[1]])
                    else:
                        for i in range(len(self.text_lines[self.cursor_pos[1]])):
                            w1 = self.font.render(self.text_lines[self.cursor_pos[1]][:i + 1], 1, self.font_color).get_width()
                            w0 = self.font.render(self.text_lines[self.cursor_pos[1]][:i], 1, self.font_color).get_width()
                            if mp[0] < self.text_x + w1:
                                if mp[0] < self.text_x + w0 + (w1 - w0) / 2:
                                    self.cursor_pos[0] = i
                                else:
                                    self.cursor_pos[0] = i + 1
                                break
                    #
                    self.cursor = 0
                    for i in range(self.cursor_pos[1]):
                        self.cursor += len(self.text_lines[i]) + 1
                    self.cursor += self.cursor_pos[0]
            else:
                self.image = self.hover_image
                if self.mouselast and self.input_manager.mousetag_object[0] == self:
                    self.input_manager.mouse_connect_object[0] = self
            self.mouselast = mousedown
        else:
            if self.input_manager.mousetag_object[0] == self:
                self.input_manager.mouse_connect_object[0] = self
            if not mousedown:
                self.image = self.inactive_image
            if mousedown and self.input_manager.mouse_connect_object[0] == self:
                self.input_manager.mouse_connect_object[0] = None
                if str(type(self.onsubmit)) == "<class 'function'>":
                    if self.onsubmit_params != None:
                        self.onsubmit(*self.onsubmit_params)
                    else:
                        self.onsubmit()
        #
        if self.input_manager.mouse_connect_object[0] == self:
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT and self.cursor >= 1:
                        self.cursor -= 1
                    if event.key == pygame.K_RIGHT and self.cursor < len(self.text):
                        self.cursor += 1
                    if event.key == pygame.K_BACKSPACE and self.cursor > 0:
                        self.text = self.text[:self.cursor - 1] + self.text[self.cursor:]
                        self.cursor -= 1
                    if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                        if (len(self.text_lines) + 1) * self.h < self.rect.h - self.text_y * 2:
                            self.text = self.text[:self.cursor] + "\n" + self.text[self.cursor:]
                            self.cursor += 1
                    elif event.unicode != "" and event.key != pygame.K_ESCAPE and event.key != pygame.K_DELETE and event.key != pygame.K_BACKSPACE and event.key != pygame.K_RETURN and event.key != pygame.K_KP_ENTER:
                        if (self.enabled_symbols == None or event.unicode in self.enabled_symbols) and not (event.unicode in self.disabled_symbols):
                            text_img = self.font.render(self.text_lines[self.cursor_pos[1]] + event.unicode, True, self.font_color)
                            if text_img.get_width() < self.rect.w - self.text_x * 2:
                                self.text = self.text[:self.cursor] + event.unicode + self.text[self.cursor:]
                                self.cursor += 1
            #
            l = 0
            for i in range(len(self.text_lines)):
                l += len(self.text_lines[i]) + 1
                if self.cursor < l:
                    self.cursor_pos = [len(self.text_lines[i]) - (l - self.cursor) + 1, i]
                    break
        #
        if last_text != self.text:
            self.update_text_image()
            if self.color_text != None:
                self.colors = self.color_text(self.text_lines)
            if str(type(self.onchange)) == "<class 'function'>":
                if self.onchange_params != None:
                    self.onchange(*self.onchange_params)
                else:
                    self.onchange()

    def update_text_image(self):
        text = self.text.split("\n")
        ins = []
        for i in range(len(text)):
            t = text[i]
            while self.font.render(text[i], 1, self.font_color).get_width() > self.rect.w - self.text_x * 2:
                tn = ""
                for j in range(len(t)):
                    tn += t[j]
                    if self.font.render(tn, 1, self.font_color).get_width() > self.rect.w - self.text_x * 2:
                        text[i] = t[j:]
                        t = text[i]
                        ins.append((i - 1, tn[:-1]))
                        break
        for i in ins:
            text.insert(i[0], i[1])
        self.text_lines = text

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        h = 0
        for i in range(len(self.text_lines)):
            t = self.text_lines[i]
            render_colored_text(t, (self.rect.x + self.text_x, self.rect.y + self.text_y + h), screen, font=self.font, base_color=self.font_color, colors=self.colors[i])
            h += self.h
        if self.input_manager.mouse_connect_object[0] == self and self.timer > 30:
            text_img = self.font.render(self.text_lines[self.cursor_pos[1]][:self.cursor_pos[0]], True, self.font_color)
            pygame.draw.rect(screen, self.font_color, (self.rect.x + self.text_x + text_img.get_width(), self.rect.y + self.text_y + self.cursor_pos[1] * self.h, 2, text_img.get_height()))

    def add_enabled_symbols(self, e):
        self.enabled_symbols = e

    def add_disabled_symbols(self, d):
        self.disabled_symbols = d

    def add_onclick(self, p):
        self.onclick = p

    def add_onclick_params(self, p):
        self.onclick_params = p

    def add_onchange(self, p):
        self.onchange = p

    def add_onchange_params(self, p):
        self.onchange_params = p

    def add_onsubmit(self, p):
        self.onsubmit = p

    def add_onsubmit_params(self, p):
        self.onsubmit_params = p

    def add_color_text(self, p):
        self.color_text = p

    def get_text(self):
        return(self.text)

    def set_text(self, text):
        self.text = text