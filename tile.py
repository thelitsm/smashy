import pygame
import random

from unit import *
from display import *


class Tile:
    def __init__(self, x, y, tile_type, tile_level, image_path):
        self.x = x
        self.y = y
        self.tile_type = tile_type  # Type de la case (normal, infranchissable, etc.)
        self.tile_level = tile_level # Niveau de la case ('0' ou 'escalier' ou '1')
        self.image = pygame.image.load(image_path)  # Charger l'image
        self.image = pygame.transform.scale(self.image, (CELL_SIZE, CELL_SIZE))  # Ajuster la taille

    def draw(self, screen):
        screen.blit(self.image, (self.x * CELL_SIZE, self.y * CELL_SIZE))
