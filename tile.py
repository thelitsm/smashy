import pygame
import random

from unit import *
from display import *

CELL_SIZE = 40

class Tile:
    def __init__(self, x, y, tile_type, is_walkable, image_path=None):
        self.x = x
        self.y = y
        self.tile_type = tile_type  # Type de la case (normal, mur, miel, eau, ou vitesse)
        self.walkable = is_walkable  # Les unités peuvent-elles s'y déplacer ?
        self.image_path = image_path  # Chemin de l'image de la case (optionnel)

    def draw(self, screen):
        if self.image_path:
            # Redimensionner l'image pour qu'elle tienne dans une cellule
            image = pygame.image.load(self.image_path)
            image = pygame.transform.scale(image, (CELL_SIZE, CELL_SIZE))  # Ajuste l'image à la taille de la cellule
            screen.blit(image, (self.x * CELL_SIZE, self.y * CELL_SIZE))  # Affiche l'image à la position (x, y)

class Miel(Tile):
    def __init__(self, x, y, tile_type, is_walkable, image_path):
        super().__init__(x=x, y=y, tile_type = 'miel', is_walkable = True, image_path = 'assets/cases/miel.png')

class Vitesse(Tile):
    def __init__(self, x, y, tile_type, is_walkable, image_path):
        super().__init__(x=x, y=y, tile_type='vitesse', is_walkable='yes', image_path='assets/cases/eclair.png')
        self.speed_modifier = random.randint(-1, 2)  # Modifie la vitesse entre -1 et +2

    def get_speed_modifier(self):
        return self.speed_modifier

class Eau(Tile):
    def __init__(self, x, y, tile_type, is_walkable, image_path):
        super().__init__(x=x, y=y, tile_type='eau', is_walkable=True, image_path='assets/cases/eau.png')
        self.allowed_characters = ['sucette volante', 'jus d\'orange']  # Seulement ces personnages peuvent y passer

    def can_pass(self, character):
        return character in self.allowed_characters

class Orange(Tile):
    def __init__(self, x, y, tile_type, is_walkable):
        super().__init__(x=x, y=y, tile_type='orange', is_walkable=True)
        self.hp_adder = random.randint(1, 4)  # Ajoute des hp entre 1 et 4

    def get_hp_adder(self):
        return self.hp_adder
