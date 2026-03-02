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

def render_text(text, pos, screen, color=(0, 0, 0), centerx="left", centery="up", font=None, font_name=None, font_size=24, font_alpha=True):#отрисовка текста на экране
    if font == None:
        font = pygame.font.SysFont(font_name, font_size)
    text_img = font.render(text, font_alpha, color)
    text_rect = text_img.get_rect()
    if centerx == "left":
        text_rect.x = pos[0]
    elif centerx == "center":
        text_rect.centerx = pos[0]
    elif centerx == "right":
        text_rect.x = pos[0] - text_img.get_width()
    if centery == "up":
        text_rect.y = pos[1]
    elif centery == "center":
        text_rect.centery = pos[1]
    elif centery == "down":
        text_rect.y = pos[1] - text_img.get_height()
    screen.blit(text_img, text_rect)