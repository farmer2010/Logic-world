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

def render_text(text, pos, screen, color=(0, 0, 0), outline_color=(255, 255, 255), center=(0, 0), font=None, font_name=None, font_size=24, font_alpha=True, outline_size=0, alpha=255):#отрисовка текста на экране
    if font == None:
        font = pygame.font.SysFont(font_name, font_size)
    text_img = font.render(text, font_alpha, color)
    #
    pos = list(pos)
    pos[0] -= text_img.get_width() * center[0]
    pos[1] -= text_img.get_height() * center[1]
    #
    img = pygame.Surface((text_img.get_width() + outline_size * 2, text_img.get_height() + outline_size * 2), pygame.SRCALPHA)
    img.fill((0, 0, 0, 0))
    out_img = font.render(text, font_alpha, outline_color)
    for x in range(-outline_size, outline_size + 1, 1):
        for y in range(-outline_size, outline_size + 1, 1):
            if x != 0 and y != 0:
                img.blit(out_img, (outline_size + x, outline_size + y))
    img.blit(text_img, (outline_size, outline_size))
    #
    img.set_alpha(alpha)
    #
    screen.blit(img, (pos[0] - outline_size, pos[1] - outline_size))