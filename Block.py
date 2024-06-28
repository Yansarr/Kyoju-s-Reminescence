import pygame
import pygame as pg
from os.path import isfile, join

from Object import Object
import pytmx


def get_block(width, height):
    path = join("assets", "Terrain", "Terrain.png")
    image = pg.image.load(path).convert_alpha()
    surface = pg.Surface((width, height), pg.SRCALPHA, 32)
    rect = pg.Rect(0, 0, width, height)
    surface.blit(image, (0, 0), rect)
    return surface


class Block(Object):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        block = get_block(width, height)
        self.image.blit(block, (0, 0))
        self.mask = pg.mask.from_surface(self.image)
