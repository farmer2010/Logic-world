import pygame
from block import Block
from image_factory import *

class PistonHead(Block):
    def __init__(self, world, pos, glassed=0, data=None):
        preset_data = {"rotate" : 0, "sticky" : 0}
        Block.__init__(self, world, pos, "piston head", glassed, data, preset_data)

    def get_pushable(self, rotate):
        return(0)

    def get_image(self):
        return(get_image(self.data["sticky"], 12 + self.data["rotate"], size=self.world.block_scale))