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

def get_wire_image(neighbours, data):
    return(get_image(6 + neighbours[0] * 2 + neighbours[3] + 4 * data["activated"], neighbours[2] * 2 + neighbours[1]))

def get_activator_image(data):
    return(get_image(data["activated"], 2))