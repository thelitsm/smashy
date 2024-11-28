import pygame
import random

from unit import *
from display import *


class Tile:
    def __init__(self, x, y, tile_type, is_walkable):
        self.x = x
        self.y = y
        self.tile_type = tile_type  # Type de la case (normal ou mur)
        self.walkable = is_walkable # Les unités peuvent-elles s'y déplacer ? (bool)

    # def draw(self, screen):
    #     screen.blit(self.image, (self.x * CELL_SIZE, self.y * CELL_SIZE))
