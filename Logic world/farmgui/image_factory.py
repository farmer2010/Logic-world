from farmgui.utils import *
import pygame
pygame.init()

def get_button_image(w, h, type, color, offset=3, ch=30, text="", font=pygame.font.SysFont(None, 24), font_color=(0, 0, 0)):
    img = pygame.Surface((w, h), pygame.SRCALPHA)
    if type == 0 or type == 2:
        img.fill((min(color[0] + ch, 255), min(color[1] + ch, 255), min(color[2] + ch, 255)))
        pygame.draw.rect(img, (max(color[0] - ch, 0), max(color[1] - ch, 0), max(color[2] - ch, 0)), (offset, offset, w - offset, h - offset))
        pygame.draw.rect(img, color, (offset, offset, w - offset * 2, h - offset * 2))
    elif type == 1:
        img.fill((max(color[0] - ch, 0), max(color[1] - ch, 0), max(color[2] - ch, 0)))
        pygame.draw.rect(img, (min(color[0] + ch, 255), min(color[1] + ch, 255), min(color[2] + ch, 255)), (offset, offset, w - offset, h - offset))
        pygame.draw.rect(img, color, (offset, offset, w - offset * 2, h - offset * 2))
    render_text(text, (w/2, h/2), img, font_color, centerx="center", centery="center", font=font)
    return(img)

def get_text_box_image(w, h, color, offset=3, ch=30):
    img = pygame.Surface((w, h), pygame.SRCALPHA)
    img.fill((min(color[0] + ch*2, 255), min(color[1] + ch*2, 255), min(color[2] + ch*2, 255)))
    pygame.draw.rect(img, (max(color[0] - ch, 0), max(color[1] - ch, 0), max(color[2] - ch, 0)), (offset, offset, w - offset*2, h - offset*2))
    pygame.draw.rect(img, (min(color[0] + ch, 255), min(color[1] + ch, 255), min(color[2] + ch, 255)), (offset*2, offset*2, w - offset*3, h - offset*3))
    pygame.draw.rect(img, color, (offset*2, offset*2, w - offset*4, h - offset*4))
    return(img)

def get_slider_image(w, h, color, offset=3, ch=30):
    img = pygame.Surface((w, h), pygame.SRCALPHA)
    img.fill((min(color[0] + ch * 2, 255), min(color[1] + ch * 2, 255), min(color[2] + ch * 2, 255)))
    pygame.draw.rect(img, (max(color[0] - ch, 0), max(color[1] - ch, 0), max(color[2] - ch, 0)), (offset, offset, w - offset * 2, h - offset * 2))
    pygame.draw.rect(img, (min(color[0] + ch, 255), min(color[1] + ch, 255), min(color[2] + ch, 255)), (offset * 2, offset * 2, w - offset * 3, h - offset * 3))
    pygame.draw.rect(img, color, (offset * 2, offset * 2, w - offset * 4, h - offset * 4))
    return (img)