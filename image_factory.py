import pygame
pygame.init()

texture = pygame.image.load("files/images/blocks.png")

def get_image(x, y, size=40):
    x2 = x * 10
    y2 = y * 10
    img = pygame.Surface((10, 10))
    img.fill((255, 0, 128))
    img.set_colorkey((255, 0, 128))
    img.blit(texture, (-x2, -y2))
    img = pygame.transform.scale(img, (size, size))
    return(img)

def get_wire_image(data, neighbours):
    return(get_image(6 + neighbours[2] * 2 + neighbours[3] + 4 * data["activated"], neighbours[0] * 2 + neighbours[1]))

def get_activator_image(data):
    return(get_image(data["activated"], 2))

def get_NOT_image(data, neighbours):
    return(get_image(10 + data["activated"] * 2 + neighbours[0], 4 + data["rotate"]))

def get_glass_image(neighbours):
    return(get_image(2 + neighbours[0] * 2 + neighbours[3], neighbours[2] * 2 + neighbours[1]))

def get_wire_box_image(data):
    return(get_image(5, data["activated1"] + data["activated2"] * 2 + 8))

def get_AND_image(data):
    return(get_image(14 + data["activated1"] + data["activated2"] * 2, data["rotate"]))

def get_XOR_image(data):
    return(get_image(14 + data["activated1"] + data["activated2"] * 2, 4 + data["rotate"]))

def get_diode_image(data):
    return(get_image(data["activated1"] + data["activated2"] + 2, 8 + data["rotate"]))

def get_output_image(data):
    return(get_image(data["activated"], 8 + data["rotate"]))

def get_armored_wire_image(data, neighbours):
    return(get_image(2 + neighbours[2] * 2 + neighbours[3] + 4 * data["activated"], 4 + neighbours[0] * 2 + neighbours[1]))

def get_memory_image(data):
    return(get_image(data["activated1"] + data["activated2"] * 2 + data["activated"] * 4 + 6, data["rotate"] + 8))

def get_sensor_image(data):
    return(get_image(data["activated"], data["rotate"] + 4))

def get_block_image(sftype, neighbours, data):
    if sftype == "wire":
        return(get_wire_image(data, neighbours))
    elif sftype == "activator":
        return(get_activator_image(data))
    elif sftype == "block":
        return(get_image(0, 1))
    elif sftype == "NOT":
        return(get_NOT_image(data, neighbours))
    elif sftype == "wire box":
        return(get_wire_box_image(data))
    elif sftype == "AND":
        return(get_AND_image(data))
    elif sftype == "XOR":
        return(get_XOR_image(data))
    elif sftype == "glass":
        return(get_glass_image(neighbours))
    elif sftype == "diode":
        return(get_diode_image(data))
    elif sftype == "output":
        return(get_output_image(data))
    elif sftype == "armored wire":
        return(get_armored_wire_image(data, neighbours))
    elif sftype == "memory":
        return(get_memory_image(data))
    elif sftype == "sensor":
        return(get_sensor_image(data))
    elif sftype == "energy block":
        return(get_image(0, 12))
    elif sftype == "air":
        img = pygame.Surface((40, 40))
        img.set_colorkey((0, 0, 0))
        return(img)
    else:
        print(sftype)
