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
    return(get_image(2 + neighbours[0] * 2 + neighbours[3], neighbours[2] * 2 + neighbours[1]), (0, 0))

def get_wire_box_image(data):
    return(get_image(data["activated1"], 3 + data["activated2"]))

def get_AND_image(data):
    return(get_image(14 + data["activated1"] + data["activated2"] * 2, data["rotate"]))

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
    elif sftype == "air":
        img = pygame.Surface((40, 40))
        img.set_colorkey((0, 0, 0))
        return(img)
