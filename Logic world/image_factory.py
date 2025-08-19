from utils import *
import pygame
pygame.init()

texture = pygame.image.load("files/images/blocks.png")
texture_ui = pygame.image.load("files/images/ui.png")

def get_image(x, y, size=40, txtr=texture):
    x2 = x * 10
    y2 = y * 10
    img = pygame.Surface((10, 10), flags=pygame.SRCALPHA)
    img.blit(txtr, (-x2, -y2))
    img = pygame.transform.scale(img, (size, size))
    return(img)

def get_button_image(w, h, type, text=None, size=40):
    img = pygame.Surface((w * size, h * size), flags=pygame.SRCALPHA)
    for x in range(w):
        for y in range(h):
            n = [y < h - 1, x < w - 1, y > 0, x > 0]
            st = get_image(n[0] * 2 + n[3] + type * 4, n[2] * 2 + n[1], size=size, txtr=texture_ui)
            img.blit(st, (x * size, y * size))
    if (text != None):
        img.blit(text, (0, 0))
    return(img)

def get_wire_image(data, neighbours, size=40):
    return(get_image(8 + neighbours[2] * 2 + neighbours[3] + 4 * data["activated"], neighbours[0] * 2 + neighbours[1], size=size))

def get_activator_image(data, size=40):
    return(get_image(data["activated"], 2, size=size))

def get_NOT_image(data, neighbours, size=40):
    return(get_image(12 + data["activated"] * 2 + neighbours[0], 4 + data["rotate"], size=size))

def get_glass_image(neighbours, size=40):
    return(get_image(4 + neighbours[0] * 2 + neighbours[3], neighbours[2] * 2 + neighbours[1], size=size))

def get_wire_box_image(data, size=40):
    return(get_image(7, data["activated1"] + data["activated2"] * 2 + 8, size=size))

def get_AND_image(data, size=40):
    return(get_image(16 + data["activated1"] + data["activated2"] * 2, data["rotate"], size=size))

def get_XOR_image(data, size=40):
    return(get_image(16 + data["activated1"] + data["activated2"] * 2, 4 + data["rotate"], size=size))

def get_diode_image(data, size=40):
    return(get_image(4 + data["activated1"] + data["activated2"], 8 + data["rotate"], size=size))

def get_output_image(data, size=40):
    return(get_image(data["activated"], 4 + data["rotate"], size=size))

def get_armored_wire_image(data, neighbours, size=40):
    return(get_image(4 + neighbours[2] * 2 + neighbours[3] + 4 * data["activated"], 4 + neighbours[0] * 2 + neighbours[1], size=size))

def get_memory_image(data, size=40):
    p = data["activated1"] + data["activated2"] * 2 + data["activated"] * 4
    return(get_image(8 + p - 1 * (p > 2) - 1 * (p > 4), data["rotate"] + 8, size=size))

def get_sensor_image(data, size=40):
    return(get_image(2 + data["activated"], 4 + data["rotate"], size=size))

def get_piston_image(data, size=40):
    return(get_image(data["activated"], 8 + data["rotate"], size=size))

def get_no_pushable_image(neighbours, size=40):
    return(get_image(neighbours[2] * 2 + neighbours[3], 12 + neighbours[0] * 2 + neighbours[1], size=size))

def get_block_image(sftype, neighbours, data, size=40):
    if sftype == "wire":
        return(get_wire_image(data, neighbours, size=size))
    elif sftype == "activator":
        return(get_activator_image(data, size=size))
    elif sftype == "block":
        return(get_image(0, 1, size=size))
    elif sftype == "NOT":
        return(get_NOT_image(data, neighbours, size=size))
    elif sftype == "wire box":
        return(get_wire_box_image(data, size=size))
    elif sftype == "AND":
        return(get_AND_image(data, size=size))
    elif sftype == "XOR":
        return(get_XOR_image(data, size=size))
    elif sftype == "glass":
        return(get_glass_image(neighbours, size=size))
    elif sftype == "diode":
        return(get_diode_image(data, size=size))
    elif sftype == "output":
        return(get_output_image(data, size=size))
    elif sftype == "armored wire":
        return(get_armored_wire_image(data, neighbours, size=size))
    elif sftype == "memory":
        return(get_memory_image(data, size=size))
    elif sftype == "sensor":
        return(get_sensor_image(data, size=size))
    elif sftype == "energy block":
        return(get_image(1, 3, size=size))
    elif sftype == "button":
        return(get_image(0, 3, size=size))
    elif sftype == "piston":
        return(get_piston_image(data, size=size))
    elif sftype == "no pushable":
        return(get_no_pushable_image(neighbours, size=size))
    elif sftype == "air":
        img = pygame.Surface((size, size))
        img.set_colorkey((0, 0, 0))
        return(img)
    else:
        print(sftype)