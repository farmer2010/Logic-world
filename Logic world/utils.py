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

def render_text(text, pos, screen, color=(0, 0, 0), outline_color=(255, 255, 255), center=(0, 0), font=None, font_name=None, font_size=24, font_alpha=True, outline_size=0):#отрисовка текста на экране
    if font == None:
        font = pygame.font.SysFont(font_name, font_size)
    text_img = font.render(text, font_alpha, color)
    #
    pos = list(pos)
    pos[0] -= text_img.get_width() * center[0]
    pos[1] -= text_img.get_height() * center[1]
    #
    img = font.render(text, font_alpha, outline_color)
    for x in range(-outline_size, outline_size + 1, 1):
        for y in range(-outline_size, outline_size + 1, 1):
            if x != 0 and y != 0:
                screen.blit(img, (pos[0] + x, pos[1] + y))
    screen.blit(text_img, pos)