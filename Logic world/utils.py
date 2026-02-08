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

def render_text(text, pos, screen, color=(0, 0, 0), centerx="left", centery="up", font=pygame.font.SysFont(None, 40), alpha=True):#отрисовка текста на экране
    text_img = font.render(text, alpha, color)
    text_rect = text_img.get_rect()
    if centerx == "left":
        text_rect.x = pos[0]
    elif centerx == "center":
        text_rect.x = pos[0] - text_img.get_width() / 2
    elif centerx == "right":
        text_rect.x = pos[0] - text_img.get_width()
    if centery == "up":
        text_rect.y = pos[1]
    elif centery == "center":
        text_rect.y = pos[1] - text_img.get_height() / 2
    elif centery == "down":
        text_rect.y = pos[1] - text_img.get_height()
    screen.blit(text_img, text_rect)

def get_button_image2(w, h, type, text=None, size=40):
    img = pygame.Surface((w * size, h * size), flags=pygame.SRCALPHA)
    for x in range(w):
        for y in range(h):
            n = [y < h - 1, x < w - 1, y > 0, x > 0]
    #        st = get_image(n[0] * 2 + n[3] + type * 4, n[2] * 2 + n[1], size=size, txtr=texture_ui)
    #        img.blit(st, (x * size, y * size))
    if (text != None):
        img.blit(text, (0, 0))
    return(img)