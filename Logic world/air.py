import pygame
from block import Block

class Air(Block):
    def __init__(self, world, pos, glassed=0, data=None):
        preset_data = {}
        Block.__init__(self, world, pos, "air", glassed, data, preset_data)

    def get_image(self):
        image = pygame.Surface((self.world.block_scale, self.world.block_scale))
        image.set_colorkey((0, 0, 0))
        return(image)