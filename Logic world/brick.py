import pygame
from block import Block
from image_factory import *

class Brick(Block):
    def __init__(self, world, pos, glassed=0, data=None):
        preset_data = {}
        Block.__init__(self, world, pos, "block", glassed, data, preset_data)

    def get_image(self):
        return(get_image(0, 1, size=self.world.block_scale))