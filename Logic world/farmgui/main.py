from gui import *
import pygame
pygame.init()

screen = pygame.display.set_mode((1920, 1080))
pygame.display.set_caption("GUI test")
keep_going = 1
timer = pygame.time.Clock()

def colors(text_lines):
    orange_letters = ["for", "in", "if", "elif", "else", "def", "lambda", "return", "try", "except", "pass", "class", "from", "import", "break", "and", "or", "not", "while", "None", "True", "False"]
    purple_letters = ["range", "open", "print", "str", "int", "list", "float", "len"]
    bord_symbols = [" ", "\n", "(", ")", "=", ":", "[", "]", "!", ">", "<", ",", "{", "}", ".", "+", "-", "/", "*", "#"]
    string_bord_symbols = ["'", '"']
    ret = []
    for i in range(len(text_lines)):
        type = None
        ind = 0
        tst = ""
        ret.append([])
        for j in range(len(text_lines[i]) + 1):
            if j < len(text_lines[i]):
                t = text_lines[i][j]
            else:
                if type == None:
                    t = " "
                elif type == "text":
                    t = '"'
            if t in string_bord_symbols:
                if type == None:
                    type = "text"
                elif type == "text":
                    type = None
                    if tst != "":
                        ret[i].append([ind, j + 1, (0, 100, 0), tst])
                ind = j
                tst = ""
            if t in bord_symbols and type == None:
                if tst != "":
                    try:
                        int(tst)
                        ret[i].append([ind, j, (0, 80, 255), tst])
                    except:
                        if tst in orange_letters:
                            ret[i].append([ind, j, (255, 100, 0), tst])
                        if tst in purple_letters:
                            ret[i].append([ind, j, (100, 0, 100), tst])
                ind = j + 1
                tst = ""
            if t == "#" and type == None:
                ret[i].append([ind - 1, len(text_lines[i]), (230, 0, 0), tst])
                break
            if not t in bord_symbols:
                tst += t
    return(ret)

buttons = ButtonManager(background_color=(255, 255, 255))
#
buttons.add(Button((50, 50, 200, 50), onrelease=lambda: print(1)))
buttons.add(TextBox((50, 150, 200, 50)))
buttons.add(Slider((50, 250, 200, 50), (44, 44)))
buttons.add(RadioButton((50, 350, 30, 30)))
#
panel = Panel((500, 100, 300, 600), background_color=(180, 180, 180))
panel.add(Button((5, 5, 250, 35), text="button 1"))
panel.add(Button((5, 45, 250, 35), text="button 2"))
panel.add(Button((5, 85, 250, 35), text="button 3"))
buttons.add(panel)
#
group = RadioButtonGroup()
buttons.add(RadioButton((50, 400, 30, 30), selected=1, group=group, text="1"))
buttons.add(RadioButton((50, 440, 30, 30), group=group, text="2"))
buttons.add(RadioButton((50, 480, 30, 30), group=group, text="3"))
buttons.add(RadioButton((50, 520, 30, 30), group=group, text="4"))
#
buttons.add(TextLabel("Hello world!", (0, 0), font_color=(0, 128, 255)))
label = TextLabel("", (0, 30))
label.add_update_text(lambda: "value: " + str(buttons.get_component(2).get_value()))
buttons.add(label)
#
slider = Slider((275, 250, 200, 50), (44, 44))
slider.add_update_text(lambda x: "value: " + str(x))
buttons.add(slider)
#
buttons.add(NumberBox((50, 570, 70, 28), preset_value=10, max_value=10, change_value=1))
buttons.add(NumberBox((150, 570, 70, 28), preset_value=5, max_value=10, change_value=0.1))
#
buttons.add(TextField((900, 100, 400, 600), font=pygame.font.Font("D:/Source_Code_Pro/static/SourceCodePro-Medium.ttf", 14), color_text=colors))

while keep_going:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            keep_going = 0
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                keep_going = 0
    #
    screen.fill((255, 255, 255))
    buttons.update(screen, events)
    pygame.display.update()
    timer.tick(60)
pygame.quit()