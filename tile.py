import pygame
import random

from unit import *
from abc import ABC, abstractmethod

CELL_SIZE = 40

class AbstractTile(ABC):
    def __init__(self, x, y, tile_type, is_walkable, image_path=None, allowed_characters = ['Sucette Volante', 'Jus orange']):
        self.x = x
        self.y = y
        self.tile_type = tile_type  # Type de la case (normal, mur, miel, eau, ou vitesse)
        self.walkable = is_walkable  # Les unités peuvent-elles s'y déplacer ?
        self.image_path = image_path  # Chemin de l'image de la case (optionnel)
        self.allowed_characters = allowed_characters 

    @abstractmethod
    def apply_effect(self, unit):
        """
        Méthode abstraite pour appliquer un effet spécifique à la tuile.
        """
        pass

    def draw(self, screen):
        if self.image_path:
            image = pygame.image.load(self.image_path)
            image = pygame.transform.scale(image, (CELL_SIZE, CELL_SIZE))
            screen.blit(image, (self.x * CELL_SIZE, self.y * CELL_SIZE))

class GenericTile(AbstractTile):
    def __init__(self, x, y, tile_type, is_walkable, image_path=None):
        super().__init__(x, y, tile_type, is_walkable, image_path)

    def apply_effect(self, unit):
        """
        Implémentation par défaut : aucune action spécifique.
        """
        pass


class Miel(AbstractTile):
    def __init__(self, x, y, tile_type, is_walkable, image_path):
        super().__init__(x=x, y=y, tile_type = 'miel', is_walkable = True, image_path = 'assets/cases/miel.png')

    def apply_effect(self, unit):
        """
        Bloque le mouvement de l'unité pour ce tour.
        """
        print(f"{unit.unit_type} est bloqué sur une case de miel !")
        unit.moves = 0  # Réduit les mouvements restants à 0
        unit.health -= 2 # Enlève deux points de vie 

class Vitesse(AbstractTile):
    def __init__(self, x, y, tile_type, is_walkable, image_path):
        super().__init__(x=x, y=y, tile_type='vitesse', is_walkable='yes', image_path='assets/cases/eclair.png')

    def apply_effect(self, unit):
        """
        Ajoute de la vitesse à l'unité si elle n'est pas à pleine santé.
        """
        if unit.speed < unit.max_speed:  # Vérifie si la vitesse peut être augmentée
            speed_modifier = random.choice([-1, 1, 2])  # Les valeurs possibles sont -1, 1, et 2
            speed_before = unit.speed
            unit.speed = min(speed_before + speed_modifier, unit.max_speed)  # Limite la vitesse
            unit.speed = max(speed_before + speed_modifier, unit.min_speed) #Garantit au moins une vitesse de 1
            print(f"{unit.unit_type} a gagné {speed_modifier} et est mtn a {unit.speed} et au cs as ou {unit.max_speed}")
        else :
            print("t'as deja la  vitesse max ja7ech")

class Eau(AbstractTile):
    def __init__(self, x, y, tile_type, is_walkable, image_path):
        super().__init__(x=x, y=y, tile_type='eau', is_walkable=True, image_path='assets/cases/eau.png')

    def can_pass(self, character):
        return character in self.allowed_characters
    
    def apply_effect(self, unit):
        """
        Applique un effet spécifique lorsque l'unité interagit avec une case d'eau.
        Dans ce cas, il n'y a pas d'effet particulier, sauf restriction pour certains types d'unités.
        """
        pass

class Orange(AbstractTile):
    def __init__(self, x, y, tile_type, is_walkable, image_path):
        super().__init__(x=x, y=y, tile_type='orange', is_walkable=True, image_path='assets/cases/orange.png')

    def apply_effect(self, unit):
        """
        Ajoute des HP à l'unité si elle n'est pas à pleine santé.
        """
        if unit.health < unit.max_health:  # Vérifie si les HP peuvent être augmentés
            hp_adder = random.randint(1, 4)  # Ajoute des hp entre 1 et 4
            health_before = unit.health
            unit.health = min(health_before + hp_adder, unit.max_health)  # Limite à la santé maximale
            unit.health = max(health_before + hp_adder, 0)  # Limite à 0 HP minimum

